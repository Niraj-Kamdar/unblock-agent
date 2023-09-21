import json
import secrets
import openai
from fastapi import FastAPI, Security, WebSocket
from typing import Any

from .chat import Chat
from .constants import OPENAI_API_KEY, SANITY_LIMIT
from .agent import get_agent_response
from .auth import get_api_key, validate_api_key
from .crud import get_invocation, get_chat_from_socket
from .schemas import (
    ChatCreatedResponse,
    CreateChatRequest,
    AgentResponse,
    UserMessage,
    UserMessageType,
)

openai.api_key = OPENAI_API_KEY
app = FastAPI()


@app.post("/chats", response_model=ChatCreatedResponse, status_code=201, tags=["chats"])
async def create_chat(request: CreateChatRequest):
    """
    Create a new chat session.

    Create and initiate a new chat session. This endpoint returns a unique chat_id
    which can be used for further interactions in the chat session.
    """
    chat_id = secrets.token_urlsafe(16)
    chat = await Chat.from_db(chat_id, request.prompt)
    agent_response = await get_agent_response(chat, UserMessage(type=UserMessageType.NONE, content=""))
    return ChatCreatedResponse(
        chat_id=chat.id,
        prompt=chat.prompt,
        agent_response=agent_response,
    )


@app.put("/chats/{chat_id}", response_model=AgentResponse, tags=["chats"])
async def send_message(
    chat_id: str, request: UserMessage, api_key: str = Security(get_api_key)
):
    """
    Send a message to a chat session.

    Use this endpoint to send a message to a chat session and get a response.
    The chat_id is used to identify the chat session.
    """

    chat = await Chat.from_db(chat_id)
    return await get_agent_response(chat, request)


@app.websocket("/chats/{chat_id}")
async def chat_socket(
    websocket: WebSocket,
    chat_id: str,
):
    validate_api_key(websocket)

    await websocket.accept(chat_id)

    chat = await get_chat_from_socket(websocket, chat_id)
    functions = await chat.functions()

    while chat.messages[-1]["content"] != "DONE" and chat.sanity_counter < SANITY_LIMIT:
        completion: Any = await openai.ChatCompletion.acreate(  # type: ignore
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
            function_parameters = json.loads(
                model_message["function_call"]["arguments"]
            )

            try:
                invocation = await get_invocation(function_name, function_parameters)
                await websocket.send_text(
                    json.dumps(
                        {"role": "assistant", "invocation": True, "content": invocation}
                    )
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

    uvicorn.run(app, host="0.0.0.0", port=8000)  # type: ignore
