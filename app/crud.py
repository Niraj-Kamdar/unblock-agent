import json
from fastapi import WebSocket
import jsonschema
from typing import Any

from .chat import Chat, ChatAndPromptNotFound
from .database import functions_collection


async def load_functions(ids: list[str]) -> list[Any]:
    # Fetch documents by their IDs
    cursor = functions_collection.find({"_id": {"$in": ids}})
    return await cursor.to_list(length=None)  # type: ignore


async def load_functions_by_namespace(namespace: str) -> list[Any]:
    # Use a regex to find documents with _id starting with 'prefix_'
    cursor = functions_collection.find({"_id": {"$regex": f"^{namespace}_"}})
    return await cursor.to_list(length=None)  # type: ignore


async def get_invocation(
    function_name: str, function_parameters: dict[str, Any]
) -> dict[str, Any]:
    function = await functions_collection.find_one({"_id": function_name})
    if not function:
        raise ValueError(f"Function {function_name} not found")

    parameters_schema = function["schema"]["parameters"]
    jsonschema.validate(function_parameters, parameters_schema)

    invocation = function["invocation"]
    invocation["args"] = json.loads(invocation["args"].format(**function_parameters))
    return invocation


async def get_chat_from_socket(websocket: WebSocket, chat_id: str):
    try:
        return await Chat.from_db(chat_id)
    except ChatAndPromptNotFound:
        prompt = await websocket.receive_text()
        return await Chat.from_db(chat_id, prompt)
