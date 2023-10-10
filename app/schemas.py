from enum import Enum
from typing import Any, Optional

from pydantic import BaseModel, Field
from pydantic.alias_generators import to_camel


class UserMessageType(str, Enum):
    ABORT = "ABORT"
    MESSAGE = "MESSAGE"
    FUNCTION = "FUNCTION"
    NONE = "NONE"


class AgentResponseType(str, Enum):
    MESSAGE = "MESSAGE"
    INVOCATION = "INVOCATION"
    ERROR = "ERROR"
    VALIDATION = "VALIDATION"
    END = "END"


class CamelModel(BaseModel):
    class Config:
        alias_generator = to_camel
        populate_by_name = True

    @classmethod
    def get_example(cls, index: int = 0) -> dict[str, Any]:
        """
        Get examples by index for the entire model.

        Args:
        - index: The index of the example set (default is 0).

        Returns:
        - Dictionary with examples for each field.
        """
        example: dict[str, Any] = {}
        for field_name, field in cls.__fields__.items():
            example_list = field.examples
            if example_list and 0 <= index < len(example_list):
                example[field_name] = example_list[index]

        return cls(**example).model_dump()

    @classmethod
    def examples(cls) -> list[dict[str, Any]]:
        min_examples = min(
            map(lambda f: len(f.examples) if f.examples else 0, cls.__fields__.values())
        )
        return [cls.get_example(i) for i in range(min_examples)]


class Invocation(CamelModel):
    uri: str = Field(..., examples=["wrap://wrapscan.io/polywrap/ens@1.0"])
    method: str = Field(..., examples=["getOwner"])
    args: dict[str, Any] = Field(..., examples=[{"domain": "vitalik.eth"}])


class InvocationContent(CamelModel):
    function_name: str = Field(..., examples=["ens_getOwner"])
    invocation: Invocation = Field(..., examples=[Invocation.get_example(0)])
    description: str = Field(..., examples=["Get the owner of vitalik.eth"])
    require_sign: bool = Field(..., examples=[False])


class ValidationContent(CamelModel):
    function_name: str = Field(..., examples=["ens_getOwner"])
    arguments: dict[str, Any] = Field(..., examples=[{"domain": "vitalik"}])
    error: str = Field(
        ..., examples=["String 'vitalik' does not match regex pattern '^(.*\\.eth)$'."]
    )


class ErrorType(str, Enum):
    SANITY_LIMIT = "SANITY_LIMIT"
    FUNCTION_NAME_REQUIRED = "FUNCTION_NAME_REQUIRED"


class ErrorContent(CamelModel):
    error: ErrorType = Field(..., examples=["SANITY_LIMIT"])


class AgentResponse(CamelModel):
    type: AgentResponseType = Field(
        ..., examples=["INVOCATION", "VALIDATION", "ERROR", "MESSAGE", "END"]
    )
    invocation: Optional[InvocationContent] = Field(
        None, examples=[InvocationContent.get_example(0), None, None, None, None]
    )
    validation: Optional[ValidationContent] = Field(
        None, examples=[None, ValidationContent.get_example(0), None, None, None]
    )
    error: Optional[ErrorContent] = Field(
        None, examples=[None, None, ErrorContent.get_example(0), None, None]
    )
    message: Optional[str] = Field(
        None,
        examples=[
            None,
            None,
            None,
            "Sorry, I cannot send or manage cryptocurrencies or any other assets for you.",
            "I have sent 0.07 ether to vitalik.eth.",
        ],
    )


class ChatCreatedResponse(CamelModel):
    chat_id: str = Field(..., examples=["uxBBFbpLNuCd6jB2pQT3oB"])
    prompt: str = Field(..., examples=["Send 0.07 ETH to vitalik.eth"])
    agent_response: AgentResponse = Field(..., examples=[AgentResponse.get_example(0)])


class CreateChatRequest(CamelModel):
    prompt: str


class UserMessage(CamelModel):
    type: UserMessageType
    function_name: Optional[str] = None
    content: str
