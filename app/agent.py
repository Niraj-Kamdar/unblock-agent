import json
import openai
from typing import Any

from .constants import SANITY_LIMIT
from .crud import get_invocation
from .schemas import (
    AgentResponse,
    AgentResponseType,
    UserMessageType,
    UserMessage,
)
from .chat import Chat


async def get_agent_response(chat: Chat, message: UserMessage) -> AgentResponse:
    if chat.sanity_counter >= SANITY_LIMIT:
        return AgentResponse(type=AgentResponseType.ERROR, content="SANITY_LIMIT_REACHED")

    match message.type:
        case UserMessageType.ABORT:
            await chat.messages.append({"role": "user", "content": message.content})
            return AgentResponse(type=AgentResponseType.MESSAGE, content="ABORTED")
        case UserMessageType.MESSAGE:
            await chat.messages.append({"role": "user", "content": message.content})
        case UserMessageType.FUNCTION:
            await chat.messages.append(
                {
                    "role": "function_call",
                    "name": message.function_name,
                    "content": message.content,
                }
            )
        case UserMessageType.NONE:
            pass

    functions = await chat.functions()
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
        function_parameters = json.loads(model_message["function_call"]["arguments"])

        try:
            invocation = await get_invocation(function_name, function_parameters)
            return AgentResponse(
                type=AgentResponseType.INVOCATION,
                content=json.dumps(
                    {"function_name": function_name, "invocation": invocation}
                ),
            )
        except Exception as e:
            validation_error = {
                "role": "function",
                "name": function_name,
                "content": f"Error: {e}",
            }
            await chat.sanity_counter.increment(1)
            await chat.messages.append(validation_error)

            return AgentResponse(
                type=AgentResponseType.VALIDATION,
                content=json.dumps(
                    {
                        "name": function_name,
                        "arguments": function_parameters,
                        "error": str(e),
                    }
                ),
            )
    else:
        await chat.sanity_counter.increment(1)
        return AgentResponse(type=AgentResponseType.MESSAGE, content=model_message["content"])