import json
import openai
from fastapi import FastAPI, WebSocket
from typing import Any

from .chat import Chat, ChatAndPromptNotFound
from .constants import OPENAI_API_KEY
from .auth import validate_api_key
from .crud import get_invocation

openai.api_key = OPENAI_API_KEY
app = FastAPI()


async def get_chat(websocket: WebSocket, chat_id: str):
    try:
        return await Chat.from_db(chat_id)
    except ChatAndPromptNotFound:
        prompt = await websocket.receive_text()
        return await Chat.from_db(chat_id, prompt)


@app.websocket("/chats/{chat_id}")
async def chat_socket(
    websocket: WebSocket,
    chat_id: str,
):
    validate_api_key(websocket)

    await websocket.accept(chat_id)

    chat = await get_chat(websocket, chat_id)
    functions = await chat.functions()

    while chat.messages[-1]["content"] != "DONE" and chat.sanity_counter < 10:
        completion: Any = await openai.ChatCompletion.acreate( # type: ignore
            model="gpt-3.5-turbo-16k-0613",
            messages=list(chat.messages),
            functions=functions,
            temperature=0,
            max_tokens=500,
        )
        model_message = completion["choices"][0]["message"]
        await chat.messages.append(model_message)

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
                    await chat.messages.append({"role": "user", "content": "ABORT"})
                    break
                await chat.messages.append(
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
                await chat.sanity_counter.increment(1)
                await chat.messages.append(invocation_error_message)

                await websocket.send_text(json.dumps(invocation_error_message))
                on_error = await websocket.receive_text()
                if on_error == "ABORT":
                    await chat.messages.append({"role": "user", "content": "ABORT"})
                    break
        else:
            await chat.sanity_counter.increment(1)
            await websocket.send_text(json.dumps(model_message))

    await websocket.close()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000) # type: ignore
