from pprint import pprint
from typing import cast
from httpx import Client
import json


def http_demo():
    # Step 1: Create a chat session
    create_chat_request = dict(
        prompt="Send 5000 gwei to vitalik.eth"
    )

    print("Step 1: Create a chat session")
    print(f"Request: {create_chat_request}")

    with Client(base_url="http://0.0.0.0:8000", timeout=60) as client:
        http_response = client.post(
            "/chats?api-key=923adjhb-288cbjSudhuido-828bchbcj", json=create_chat_request
        )
    assert http_response.status_code == 201

    chat_created_response = http_response.json()
    chat_id = chat_created_response["chatId"]
    agent_response = chat_created_response["agentResponse"]

    while True:
        pprint(agent_response)
        match agent_response["type"]:
            case "END":
                break
            case "MESSAGE":
                user_message_payload = dict(
                    type="NONE",
                    content="",
                )
                with Client(
                    base_url="http://0.0.0.0:8000",
                    timeout=60,
                ) as client:
                    put_response = client.put(
                        f"/chats/{chat_id}?api-key=923adjhb-288cbjSudhuido-828bchbcj",
                        json=user_message_payload,
                    )
            case "INVOCATION":
                data = agent_response["invocation"]
                if data["invocation"]["method"] in ["getOwner", "getAddress"]:
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content="0x4675C7e5BaAFBFFbca748158bEcBA61ef3b0a263",
                    )
                elif data["invocation"]["method"] == "getBalance":
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content="0.373892",
                    )
                elif data["invocation"]["method"] == "sendTransaction":
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content="0xb0e6065efed3b1c34d5e251c5783fa5b40dbcc07a7e1d326b32b07973c34812c",
                    )
                elif data["invocation"]["method"] == "taskCompleted":
                    result = dict(
                        type="ABORT",
                        content="DONE",
                    )
                else:
                    continue
                user_message_payload = result

                pprint(user_message_payload)

                with Client(
                    base_url="http://0.0.0.0:8000",
                    timeout=60,
                ) as client:
                    put_response = client.put(
                        f"/chats/{chat_id}?api-key=923adjhb-288cbjSudhuido-828bchbcj",
                        json=user_message_payload,
                    )
                assert put_response.status_code == 200
            case _:
                raise ValueError(agent_response)
        agent_response = put_response.json()


http_demo()
