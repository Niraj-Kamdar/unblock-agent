from enum import IntEnum
from pydantic import BaseModel
from typing import Optional


class UserMessageType(IntEnum):
    ABORT = 0
    MESSAGE = 1
    FUNCTION = 2
    NONE = 3


class AgentResponseType(IntEnum):
    MESSAGE = 0
    INVOCATION = 1
    ERROR = 2
    VALIDATION = 3
    END = 4


class AgentResponse(BaseModel):
    type: AgentResponseType
    content: Optional[str] = None


class ChatCreatedResponse(BaseModel):
    chat_id: str
    prompt: str
    agent_response: AgentResponse


class CreateChatRequest(BaseModel):
    prompt: str


class UserMessage(BaseModel):
    type: UserMessageType
    function_name: Optional[str] = None
    content: str
