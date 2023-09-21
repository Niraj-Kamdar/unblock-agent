from functools import total_ordering
from typing import Any
from motor.core import AgnosticCollection


@total_ordering
class ChatCounter:
    _chat_collection: AgnosticCollection
    _value: int
    _chat_id: str
    _field_name: str

    def __init__(self, chat_collection: AgnosticCollection, chat_id: str, field_name: str, initial_value: int = 0):
        self._value = initial_value
        self._chat_id = chat_id
        self._field_name = field_name
        self._chat_collection = chat_collection

    @classmethod
    async def from_db(cls, chat_collection:  AgnosticCollection, chat_id: str, field_name: str):
        chat = await chat_collection.find_one({"_id": chat_id})
        return cls(chat_collection, chat_id, field_name, chat[field_name] if chat else 0)

    async def increment(self, amount: Any) -> "ChatCounter":
        if not isinstance(amount, int) or amount < 0:
            raise ValueError("Only positive integer increments are allowed")

        self._value += amount
        await self._chat_collection.update_one(
            {"_id": self._chat_id}, {"$inc": {self._field_name: amount}}
        )
        return self

    def __int__(self) -> int:
        return self._value

    def __str__(self) -> str:
        return str(self._value)

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ChatCounter):
            return self._value == other._value
        return self._value == other

    def __lt__(self, other: Any) -> bool:
        if isinstance(other, ChatCounter):
            return self._value < other._value
        return self._value < other
