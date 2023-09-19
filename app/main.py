import json
import os
import openai
from fastapi import FastAPI, Security, WebSocket

from .constants import (
    FT_PREDICTOR_MODEL,
    PREDICTOR_SYSTEM_PROMPT,
    UNBLOCK_AGENT_SYSTEM_PROMPT,
)
from .auth import get_api_key
from .crud import load_functions

openai.api_key = os.getenv("OPENAI_API_KEY")
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
    api_key: str = Security(get_api_key),
):
    await websocket.accept(chat_id)

    prompt = await websocket.receive_text()
    function_names = await predict_functions(prompt)
    functions = load_functions(function_names)

    messages = [
        {"role": "system", "content": UNBLOCK_AGENT_SYSTEM_PROMPT},
        {"role": "user", "content": prompt},
    ]

    await websocket.send_text(json.dumps(messages[0]))
    await websocket.send_text(json.dumps(messages[1]))

    while messages[-1]["content"] != "DONE":
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k-0613",
            messages=messages,
            functions=functions,
            temperature=0,
            max_tokens=500,
        )
        model_message = completion["choices"][0]["message"]
        messages.append(model_message)

        if model_message.get("function_call"):
            await websocket.send_text("invocation")
            function_name = model_message["function_call"]["name"]
            function_result = await websocket.receive_text()
            messages.append(
                {"role": "function", "name": function_name, "content": function_result}
            )
        else:
            await websocket.send_text(json.dumps(model_message))

    await websocket.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
