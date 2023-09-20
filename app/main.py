import json
import openai
from fastapi import Depends, FastAPI, WebSocket

from .constants import (
    FT_PREDICTOR_MODEL,
    PREDICTOR_SYSTEM_PROMPT,
    UNBLOCK_AGENT_SYSTEM_PROMPT,
    OPENAI_API_KEY,
)
from .auth import validate_api_key
from .crud import load_functions, load_functions_by_namespace, get_invocation

openai.api_key = OPENAI_API_KEY
app = FastAPI()


async def predict_functions(prompt: str):
    messages = [
        {"role": "system", "content": PREDICTOR_SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]

    predict_functions_result = await openai.ChatCompletion.acreate(
        model=FT_PREDICTOR_MODEL, messages=messages, temperature=0, max_tokens=500
    )

    predict_function = predict_functions_result["choices"][0]["message"]

    return predict_function["content"].split(", ")


@app.websocket("/chats/{chat_id}")
async def chat_socket(
    websocket: WebSocket,
    chat_id: str,
):
    validate_api_key(websocket)

    await websocket.accept(chat_id)

    prompt = await websocket.receive_text()
    function_names = await predict_functions(prompt)
    function_names = [
        function_name.replace(".", "_") for function_name in function_names
    ]
    system_functions = await load_functions_by_namespace("system")
    functions = await load_functions(function_names)
    functions.extend(system_functions)

    openai_functions = [
        function["schema"] for function in functions
    ]

    messages = [
        {"role": "system", "content": UNBLOCK_AGENT_SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]

    sanity_counter = 0

    while messages[-1]["content"] != "DONE" and sanity_counter < 10:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=messages,
            functions=openai_functions,
            temperature=0,
            max_tokens=500,
        )
        model_message = completion["choices"][0]["message"]
        messages.append(model_message)

        if model_message.get("function_call"):
            function_name = model_message["function_call"]["name"]
            function_parameters = json.loads(model_message["function_call"]["arguments"])

            try:
                invocation = await get_invocation(function_name, function_parameters)
                await websocket.send_text(
                    json.dumps({"role": "assistant", "invocation": True, "content": invocation})
                )
                function_result = await websocket.receive_text()
                if function_result == "ABORT":
                    messages.append({"role": "user", "content": "ABORT"})
                    break
                messages.append(
                    {
                        "role": "function",
                        "name": function_name,
                        "content": function_result,
                    }
                )
            except Exception as e:
                invocation_error_message = {
                    "role": "function",
                    "name": function_name,
                    "error": True,
                    "content": f"Error: {e}",
                }
                sanity_counter += 1
                messages.append(invocation_error_message)
                await websocket.send_text(json.dumps(invocation_error_message))
                on_error = await websocket.receive_text()
                if on_error == "ABORT":
                    messages.append({"role": "user", "content": "ABORT"})
                    break
        else:
            sanity_counter += 1
            await websocket.send_text(json.dumps(model_message))

    await websocket.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
