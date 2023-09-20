from typing import Iterable, Optional, TypeVar, Generic
from ..database import chat_collection

T = TypeVar('T')

class ChatList(Generic[T]):
    _items: list[T]
    _chat_id: str
    _field_name: str  # This represents the field in the chat document (e.g., "messages", "function_names", etc.)

    def __init__(self, chat_id: str, field_name: str, items: Optional[list[T]] = None):
        self._items = items or []
        self._chat_id = chat_id
        self._field_name = field_name

    @classmethod
    async def from_db(cls, chat_id: str, field_name: str):
        chat = await chat_collection.find_one({"_id": chat_id})
        return cls(chat_id, field_name, chat[field_name] if chat else [] )

    def __getitem__(self, index: int):
        return self._items[index]

    def __len__(self) -> int:
        return len(self._items)

    async def append(self, value: T) -> None:
        self._items.append(value)
        await chat_collection.update_one({"_id": self._chat_id}, {"$push": {self._field_name: value}})

    async def extend(self, values: Iterable[T]) -> None:
        self._items.extend(values)
        await chat_collection.update_one({"_id": self._chat_id}, {"$push": {self._field_name: {"$each": values}}})

    def __iter__(self):
        return iter(self._items)

    def __str__(self) -> str:
        return str(self._items)
