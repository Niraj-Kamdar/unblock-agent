import json
import traceback
from typing import Any

import openai
from motor.core import AgnosticDatabase

from .chat import Chat
from .constants import SANITY_LIMIT
from .functions import get_invocation_content
from .schemas import AgentResponse, UserMessage, UserMessageType


async def get_agent_response(
    db: AgnosticDatabase, chat: Chat, message: UserMessage
) -> AgentResponse:
    if chat.sanity_counter >= SANITY_LIMIT:
        return AgentResponse.model_validate(
            {"type": "ERROR", "error": {"error": "SANITY_LIMIT"}}
        )

    if (
        chat.messages[-1].get("function_call")
        and chat.messages[-1]["function_call"]["name"] == "system_taskCompleted"
    ):
        return AgentResponse.model_validate(
            {
                "type": "END",
                "message": json.loads(chat.messages[-1]["function_call"]["arguments"])[
                    "message"
                ],
            }
        )

    match message.type:
        case UserMessageType.ABORT:
            await chat.messages.append(
                {
                    "role": "assistant",
                    "content": None,
                    "function_call": {
                        "name": "system_taskCompleted",
                        "arguments": json.dumps(
                            {"finalMessage": f"ABORTED: {message.content}"}
                        ),
                    },
                }
            )
            return AgentResponse.model_validate(
                {"type": "END", "message": f"ABORTED: {message.content}"}
            )
        case UserMessageType.MESSAGE:
            await chat.messages.append({"role": "user", "content": message.content})
        case UserMessageType.FUNCTION:
            if not message.function_name:
                return AgentResponse.model_validate({
                    "type": "ERROR",
                    "error": {
                        "error": "FUNCTION_NAME_REQUIRED"
                    }
                })

            # print(message.function_name, message.content)

            await chat.messages.append(
                {
                    "role": "function",
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
        max_tokens=2000,
    )
    model_message = completion["choices"][0]["message"]
    await chat.messages.append(model_message)

    if model_message.get("function_call"):
        function_name = model_message["function_call"]["name"]

        # print(function_name, model_message["function_call"]["arguments"])

        function_parameters = json.loads(model_message["function_call"]["arguments"])
        try:
            content = get_invocation_content(
                function_name, function_parameters
            )
            return AgentResponse.model_validate(
                {
                    "type": "INVOCATION",
                    "invocation": content,
                }
            )
        except Exception as e:
            validation_error = {
                "role": "function",
                "name": function_name,
                "content": traceback.format_exc(),
            }
            # print(validation_error)
            await chat.sanity_counter.increment(1)
            await chat.messages.append(validation_error)

            return AgentResponse.model_validate(
                {
                    "type": "VALIDATION",
                    "validation": {
                        "function_name": function_name,
                        "arguments": function_parameters,
                        "error": f"{e.__class__.__name__}: {e}",
                    },
                }
            )
    else:
        await chat.sanity_counter.increment(1)
        await chat.messages.append(
            {
                "role": "user",
                "content": "You must call a function to achieve the given task.",
            }
        )
        return AgentResponse.model_validate(
            {"type": "MESSAGE", "message": model_message["content"]}
        )
