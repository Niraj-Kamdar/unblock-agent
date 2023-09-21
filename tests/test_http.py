from typing import cast
from fastapi.testclient import TestClient
import json

from app.main import app  # Import the FastAPI instance from your application
from app.schemas import UserMessage, UserMessageType, AgentResponse, AgentResponseType, CreateChatRequest, ChatCreatedResponse


def test_http():
    # Step 1: Create a chat session
    create_chat_request = CreateChatRequest(prompt="Send 5 ether to vitalik.eth").model_dump()
    with TestClient(app) as client:
        http_response = client.post("/chats?api-key=923adjhb-288cbjSudhuido-828bchbcj", json=create_chat_request)
    assert http_response.status_code == 201
    
    chat_created_response = ChatCreatedResponse(**http_response.json())
    chat_id = chat_created_response.chat_id
    agent_response = chat_created_response.agent_response

    while True:
        match agent_response.type:
            case AgentResponseType.MESSAGE:
                if agent_response.content == "DONE":
                    break
            case AgentResponseType.INVOCATION:
                data = json.loads(cast(str, agent_response.content))
                if data["invocation"]["method"] in ["getOwner", "getAddress"]:
                    result = UserMessage(type=UserMessageType.FUNCTION, function_name=data["function_name"], content="0xaddr81784836247647474")
                elif data["invocation"]["method"] == "getBalance":
                    result = UserMessage(type=UserMessageType.FUNCTION, function_name=data["function_name"], content="0.373892")
                elif data["invocation"]["method"] == "sendTransaction":
                    result = UserMessage(type=UserMessageType.FUNCTION, function_name=data["function_name"], content="0xtrans81784836247647827428474894474")
                else:
                    continue
                user_message_payload = result.model_dump()
                from pprint import pprint
                pprint(user_message_payload)

                with TestClient(app) as client:
                    put_response = client.put(f"/chats/{chat_id}?api-key=923adjhb-288cbjSudhuido-828bchbcj", json=user_message_payload)
                assert put_response.status_code == 200
                agent_response = AgentResponse(**put_response.json())
            case _:
                raise ValueError(agent_response)
