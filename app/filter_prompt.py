from typing import Literal, Union, cast
import openai

from .constants import (
    OPENAI_API_KEY,
    PROMPT_FILTER_AGENT,
    PROMPT_FILTER_HALLUCINATION_ANSWER,
)

openai.api_key = OPENAI_API_KEY


async def filter_prompt(
    prompt: str,
) -> Union[Literal["VALID"], Literal["INVALID"], Literal["INFO"]]:
    messages = [
        {"role": "system", "content": PROMPT_FILTER_AGENT},
        {"role": "user", "content": prompt},
    ]

    predict_functions_result: Any = await openai.ChatCompletion.acreate(  # type: ignore
        model="gpt-3.5-turbo-16k-0613", messages=messages, temperature=0, max_tokens=500
    )

    for _ in range(10):  # amount of retries
        filter_reponse = cast(str, predict_functions_result["choices"][0]["message"]["content"])
        match filter_reponse:
            case "❌":
                return "INVALID"
            case "✅":
                return "VALID"
            case "ℹ️":
                return "INFO"
            case _:
                messages.append(
                    {"role": "user", "content": PROMPT_FILTER_HALLUCINATION_ANSWER}
                )
                predict_functions_result: Any = await openai.ChatCompletion.acreate(  # type: ignore
                    model="gpt-3.5-turbo-16k-0613",
                    messages=messages,
                    temperature=0,
                    max_tokens=500,
                )
    return "INVALID"
