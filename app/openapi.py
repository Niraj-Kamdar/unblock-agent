from typing import Any

from .schemas import AgentResponse, ChatCreatedResponse


def custom_openapi_schema(default_openapi_schema: dict[str, Any]) -> dict[str, Any]:
    openapi_schema = default_openapi_schema

    openapi_schema["paths"]["/chats/{chat_id}"]["put"]["responses"]["200"]["content"][
        "application/json"
    ]["examples"] = {
        "invocation": {"summary": "Invocation", "value": AgentResponse.get_example(0)},
        "validation": {"summary": "Validation", "value": AgentResponse.get_example(1)},
        "error": {"summary": "Error", "value": AgentResponse.get_example(2)},
        "message": {"summary": "Message", "value": AgentResponse.get_example(3)},
        "end": {"summary": "End", "value": AgentResponse.get_example(4)},
    }

    chat_created_response = ChatCreatedResponse.get_example()
    openapi_schema["paths"]["/chats"]["post"]["responses"]["201"]["content"][
        "application/json"
    ]["examples"] = {
        "invocation": {
            "summary": "Invocation",
            "value": {
                **chat_created_response,
                "agent_response": AgentResponse.get_example(0),
            },
        },
        "validation": {
            "summary": "Validation",
            "value": {
                **chat_created_response,
                "agent_response": AgentResponse.get_example(1),
            },
        },
        "error": {
            "summary": "Error",
            "value": {
                **chat_created_response,
                "agent_response": AgentResponse.get_example(2),
            },
        },
        "message": {
            "summary": "Message",
            "value": {
                **chat_created_response,
                "agent_response": AgentResponse.get_example(3),
            },
        },
        "end": {
            "summary": "End",
            "value": {
                **chat_created_response,
                "agent_response": AgentResponse.get_example(4),
            },
        },
    }

    return openapi_schema