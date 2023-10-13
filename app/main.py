import json
import os
import secrets
from typing import Any

import openai
from fastapi import FastAPI, Security
from fastapi.encoders import jsonable_encoder
from fastapi.responses import HTMLResponse, JSONResponse
from motor.motor_asyncio import AsyncIOMotorClient

from .filter_prompt import filter_prompt, post_filter_response
from .agent import get_agent_response
from .auth import get_api_key
from .chat import Chat
from .constants import (
    APP_PATH,
    MONGO_URL,
    OPENAI_API_KEY,
    USER_POST_PROMPT,
)
from .openapi import custom_openapi_schema
from .schemas import (
    AgentResponse,
    ChatCreatedResponse,
    CreateChatRequest,
    UserMessage,
    UserMessageType,
)


class CamelJSONResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        json_content = jsonable_encoder(content, by_alias=True)
        return json.dumps(
            json_content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
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
    app.openapi_schema = custom_openapi_schema(default_openapi_schema)
    print("Connected to MongoDB")


@app.on_event("shutdown")
async def shutdown_event():
    global client
    client.close()
    print("Closed connection to MongoDB")


@app.get("/", response_class=HTMLResponse)
def index():
    """Index page of the website"""
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

    filter_flag = await filter_prompt(chat.prompt)
    if filter_flag != "VALID":
        return await post_filter_response(chat, filter_flag)

    agent_response = await get_agent_response(
        db,
        chat,
        UserMessage(
            type=UserMessageType.MESSAGE,
            content=f" Perform task:'{request.prompt}' {USER_POST_PROMPT}",
        ),
    )
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)  # type: ignore
