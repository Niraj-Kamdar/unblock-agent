from typing import Any, Optional, cast

from motor.core import AgnosticDatabase

from ..crud import load_functions, load_functions_by_namespace
from ..predict_functions import predict_functions
from ..constants import UNBLOCK_AGENT_SYSTEM_PROMPT
from .chat_list import ChatList
from .chat_counter import ChatCounter


class ChatAndPromptNotFound(Exception):
    """Raised when a chat is not found in the database and no prompt is provide."""


class Chat:
    id: str
    prompt: str
    sanity_counter: ChatCounter
    messages: ChatList[dict[str, Any]]
    _function_names: ChatList[str]
    _db: AgnosticDatabase

    # NOTE: do not use this constructor directly, use `Chat.from_db` instead
    def __init__(
        self,
        db: AgnosticDatabase,
        chat_id: str,
        prompt: str,
        messages: ChatList[dict[str, Any]],
        function_names: ChatList[str],
        sanity_counter: ChatCounter,
    ) -> None:
        self.id = chat_id
        self.prompt = prompt
        self.messages = messages
        self._function_names = function_names
        self.sanity_counter = sanity_counter
        self._db = db

    @classmethod
    async def from_db(
        cls,
        db: AgnosticDatabase,
        chat_id: str,
        prompt: Optional[str] = None,
    ):
        chat_collection = db["chats"]
        chat: Optional[dict[str, Any]] = await chat_collection.find_one(
            {"_id": chat_id}
        )
        if chat is None:
            if prompt is None:
                raise ChatAndPromptNotFound

            chat = {
                "_id": chat_id,
                "prompt": prompt,
                "messages": [],
                "function_names": [],
                "sanity_counter": 0,
            }
            await chat_collection.insert_one(chat)

        _prompt = prompt or cast(str, chat["prompt"])
        sanity_counter = await ChatCounter.from_db(chat_collection, chat_id, "sanity_counter")
        messages: ChatList[dict[str, Any]] = await ChatList.from_db(chat_collection, chat_id, "messages")
        if len(messages) == 0:
            await messages.extend(
                [
                    {"role": "system", "content": UNBLOCK_AGENT_SYSTEM_PROMPT},
                    {"role": "user", "content": prompt},
                ]
            )

        function_names: ChatList[str] = await ChatList.from_db(
            chat_collection,
            chat_id, "function_names"
        )
        if len(function_names) == 0:
            predicted_function_names = await predict_functions(_prompt)
            await function_names.extend(predicted_function_names)

        return cls(db, chat_id, _prompt, messages, function_names, sanity_counter)

    async def functions(self):
        functions_collection = self._db["functions"]
        system_functions = await load_functions_by_namespace(functions_collection, "system")
        functions = await load_functions(functions_collection, list(self._function_names))
        functions.extend(system_functions)

        return [function["schema"] for function in functions]
