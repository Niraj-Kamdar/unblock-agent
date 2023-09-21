from pprint import pprint
from typing import cast
from httpx import Client
import json


def http_demo():
    # Step 1: Create a chat session
    create_chat_request = dict(
        prompt="Send 5 ether to vitalik.eth"
    )
    with Client(base_url="http://localhost:8000", timeout=10) as client:
        http_response = client.post(
            "/chats?api-key=923adjhb-288cbjSudhuido-828bchbcj", json=create_chat_request
        )
    assert http_response.status_code == 201

    chat_created_response = http_response.json()
    chat_id = chat_created_response["chat_id"]
    agent_response = chat_created_response["agent_response"]

    while True:
        pprint(agent_response)
        match agent_response["type"]:
            case 4:
                break
            case 0:
                user_message_payload = dict(
                    type=3,
                    content="",
                )
                with Client(
                    base_url="http://localhost:8000",
                    timeout=10,
                ) as client:
                    put_response = client.put(
                        f"/chats/{chat_id}?api-key=923adjhb-288cbjSudhuido-828bchbcj",
                        json=user_message_payload,
                    )
            case 1:
                data = json.loads(cast(str, agent_response["content"]))
                if data["invocation"]["method"] in ["getOwner", "getAddress"]:
                    result = dict(
                        type=2,
                        function_name=data["function_name"],
                        content="0xaddr81784836247647474",
                    )
                elif data["invocation"]["method"] == "getBalance":
                    result = dict(
                        type=2,
                        function_name=data["function_name"],
                        content="0.373892",
                    )
                elif data["invocation"]["method"] == "sendTransaction":
                    result = dict(
                        type=2,
                        function_name=data["function_name"],
                        content="0xtrans81784836247647827428474894474",
                    )
                elif data["invocation"]["method"] == "taskCompleted":
                    result = dict(
                        type=0,
                        content="DONE",
                    )
                else:
                    continue
                user_message_payload = result

                pprint(user_message_payload)

                with Client(
                    base_url="http://localhost:8000",
                    timeout=10,
                ) as client:
                    put_response = client.put(
                        f"/chats/{chat_id}?api-key=923adjhb-288cbjSudhuido-828bchbcj",
                        json=user_message_payload,
                    )
                assert put_response.status_code == 200
                agent_response = put_response.json()
            case _:
                raise ValueError(agent_response)


http_demo()
