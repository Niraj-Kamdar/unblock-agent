import json
import os
import secrets
from fastapi.responses import HTMLResponse, JSONResponse
import openai
from fastapi import FastAPI, Security, WebSocket
from fastapi.encoders import jsonable_encoder
from typing import Any
from motor.motor_asyncio import AsyncIOMotorClient

from .chat import Chat, ChatAndPromptNotFound
from .constants import OPENAI_API_KEY, SANITY_LIMIT, APP_PATH, MONGO_URL
from .agent import get_agent_response
from .auth import get_api_key, validate_api_key
from .crud import get_invocation_content
from .schemas import (
    ChatCreatedResponse,
    CreateChatRequest,
    AgentResponse,
    UserMessage,
    UserMessageType,
)

class CamelJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        json_content = jsonable_encoder(content, by_alias=True)
        return json.dumps(
            json_content, ensure_ascii=False, allow_nan=False, indent=None, separators=(",", ":")
        ).encode("utf-8")


openai.api_key = OPENAI_API_KEY
app = FastAPI(default_response_class=CamelJSONResponse)
client: AsyncIOMotorClient
default_openapi_schema: dict[str, Any]

@app.on_event("startup")
async def startup_event():
    global client
    global default_openapi_schema
    client = AsyncIOMotorClient(MONGO_URL)
    default_openapi_schema = app.openapi()
    app.openapi_schema = custom_openapi_schema()
    print("Connected to MongoDB")

@app.on_event("shutdown")
async def shutdown_event():
    global client
    client.close()
    print("Closed connection to MongoDB")


def custom_openapi_schema():
    global default_openapi_schema
    openapi_schema = default_openapi_schema

    openapi_schema["paths"]["/chats/{chat_id}"]["put"]["responses"]["200"]["content"]["application/json"]["examples"] = {
        "invocation": {"summary": "Invocation", "value": AgentResponse.get_example(0)},
        "validation": {"summary": "Validation", "value": AgentResponse.get_example(1)},
        "error": {"summary": "Error", "value": AgentResponse.get_example(2)},
        "message": {"summary": "Message", "value": AgentResponse.get_example(3)},
        "end": {"summary": "End", "value": AgentResponse.get_example(4)},
    }

    chat_created_response = ChatCreatedResponse.get_example()
    openapi_schema["paths"]["/chats"]["post"]["responses"]["201"]["content"]["application/json"]["examples"] = {
        "invocation": {"summary": "Invocation", "value": {**chat_created_response, "agent_response": AgentResponse.get_example(0)}},
        "validation": {"summary": "Validation", "value": {**chat_created_response, "agent_response": AgentResponse.get_example(1)}},
        "error": {"summary": "Error", "value": {**chat_created_response, "agent_response": AgentResponse.get_example(2)}},
        "message": {"summary": "Message", "value": {**chat_created_response, "agent_response": AgentResponse.get_example(3)}},
        "end": {"summary": "End", "value": {**chat_created_response, "agent_response": AgentResponse.get_example(4)}},
    }

    return openapi_schema


@app.get("/", response_class=HTMLResponse)
def index():
    """ Index page of the website """
    index_path = os.path.join(APP_PATH, "static", "index.html")
    with open(index_path, "r") as f:
        html = f.read()
    return HTMLResponse(content=html, status_code=200)


@app.post("/chats", response_model=ChatCreatedResponse, status_code=201, tags=["chats"])
async def create_chat(request: CreateChatRequest, api_key: str = Security(get_api_key)):
    """
    Create a new chat session.

    Create and initiate a new chat session. This endpoint returns a unique chat_id
    which can be used for further interactions in the chat session.
    """
    global client
    db = client["unblock_agent_db"]

    chat_id = secrets.token_urlsafe(16)
    chat = await Chat.from_db(db, chat_id, request.prompt)
    agent_response = await get_agent_response(db, chat, UserMessage(type=UserMessageType.NONE, content=""))
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

    global client
    db = client["unblock_agent_db"]

    chat = await Chat.from_db(db, chat_id)
    return await get_agent_response(db, chat, request)


async def get_chat_from_socket(websocket: WebSocket, chat_id: str):
    global client
    db = client["unblock_agent_db"]

    try:
        return await Chat.from_db(db, chat_id)
    except ChatAndPromptNotFound:
        prompt = await websocket.receive_text()
        return await Chat.from_db(db, chat_id, prompt)


@app.websocket("/chats/{chat_id}")
async def chat_socket(
    websocket: WebSocket,
    chat_id: str,
):
    validate_api_key(websocket)

    await websocket.accept(chat_id)

    global client
    db = client["unblock_agent_db"]

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
                invocation = await get_invocation_content(db["functions"], function_name, function_parameters)
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
