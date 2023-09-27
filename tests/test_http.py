from pprint import pprint
from fastapi.testclient import TestClient

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
        pprint(agent_response)
        
        match agent_response.type:
            case AgentResponseType.END:
                break
            case AgentResponseType.MESSAGE:
                user_message_payload = dict(
                    type="NONE",
                    content="",
                )

                with TestClient(app) as client:
                    put_response = client.put(f"/chats/{chat_id}?api-key=923adjhb-288cbjSudhuido-828bchbcj", json=user_message_payload)
            case AgentResponseType.INVOCATION:
                data = agent_response.invocation
                if not data:
                    continue
                if data.invocation.method in ["getOwner", "getAddress"]:
                    result = UserMessage(type=UserMessageType.FUNCTION, function_name=data.function_name, content="0x4675C7e5BaAFBFFbca748158bEcBA61ef3b0a263")
                elif data.invocation.method == "getBalance":
                    result = UserMessage(type=UserMessageType.FUNCTION, function_name=data.function_name, content="0.373892")
                elif data.invocation.method == "sendTransaction":
                    result = UserMessage(type=UserMessageType.FUNCTION, function_name=data.function_name, content="0xb0e6065efed3b1c34d5e251c5783fa5b40dbcc07a7e1d326b32b07973c34812c")
                elif data.invocation.method == "taskCompleted":
                    result = UserMessage(
                        type=UserMessageType.FUNCTION,
                        content="DONE",
                    )
                else:
                    continue
                user_message_payload = result.model_dump(by_alias=True)

                with TestClient(app) as client:
                    put_response = client.put(f"/chats/{chat_id}?api-key=923adjhb-288cbjSudhuido-828bchbcj", json=user_message_payload)
                assert put_response.status_code == 200
                agent_response = AgentResponse(**put_response.json())
            case _:
                raise ValueError(agent_response)
        agent_response = AgentResponse(**put_response.json())
