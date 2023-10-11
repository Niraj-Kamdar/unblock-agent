from pprint import pprint
from typing import cast
from httpx import Client
import json


def http_demo():
    # Step 1: Create a chat session
    prompt = input("Enter a prompt: ")

    create_chat_request = {
        "prompt": prompt,
    }

    print("Step 1: Create a chat session")
    print(f"Request: {create_chat_request}")

    with Client(base_url="http://localhost:8000", timeout=60) as client:
        http_response = client.post(
            "/chats?api-key=923adjhb-288cbjSudhuido-828bchbcj", json=create_chat_request
        )
    pprint(http_response)
    assert http_response.status_code == 201

    chat_created_response = http_response.json()
    chat_id = chat_created_response["chatId"]
    agent_response = chat_created_response["agentResponse"]

    while True:
        pprint(agent_response)
        input("Press enter to continue...")
        match agent_response["type"]:
            case "END":
                break
            case "MESSAGE":
                user_message_payload = dict(
                    type="NONE",
                    content="",
                )
                with Client(
                    base_url="http://localhost:8000",
                    timeout=60,
                ) as client:
                    put_response = client.put(
                        f"/chats/{chat_id}?api-key=923adjhb-288cbjSudhuido-828bchbcj",
                        json=user_message_payload,
                    )
            case "VALIDATION":
                user_message_payload = dict(
                    type="NONE",
                    content="",
                )
                with Client(
                    base_url="http://localhost:8000",
                    timeout=60,
                ) as client:
                    put_response = client.put(
                        f"/chats/{chat_id}?api-key=923adjhb-288cbjSudhuido-828bchbcj",
                        json=user_message_payload,
                    )
            case "INVOCATION":
                data = agent_response["invocation"]
                if data["invocation"]["method"] in ["getOwner", "signerAddress"]:
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content="0x4675C7e5BaAFBFFbca748158bEcBA61ef3b0a263",
                    )
                elif data["invocation"]["method"] == "getSafesByOwner":
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content=json.dumps([
                            "0xa49A88055Ce0D972F6f6b9AF0843Fe4C9E9e5Ec5",
                            "0x65b9aB26803A195e4a5A435a64e1d73005f86ADD",
                            "0x176FeC0DaF2f96f2d05822a84C56bfb99002eE44",
                        ]),
                    )
                elif data["invocation"]["method"] == "deploySafe":
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content="0xa49A88055Ce0D972F6f6b9AF0843Fe4C9E9e5Ec5",
                    )
                elif data["invocation"]["method"] == "getPendingTransactions":
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content=json.dumps([
                            "0xa2f696efe1c78c823ca52e1badbaaecc95e61708913423e9baf647ebad791cd7",
                            "0xb0c589d7f025ad8396d5127bbf48c141fed2e42a5c857b42cf3d12aac2d692ee",
                            "0xf1014ca9760db3a4bb75d187606c4af0563576231a2b2d30be2aaea19321506a",
                        ]),
                    )
                elif data["invocation"]["method"] == "getSafeInfo":
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content=json.dumps({
                            "address": "0x65b9aB26803A195e4a5A435a64e1d73005f86ADD",
                            "nonce": 3,
                            "threshold": 3,
                            "owners": [
                                "0x37341cbb14c5F128A70B149726ad8B2CE6F4C793",
                                "0x639749b7b08aEe65039c21d8a411103C6ceBEBF0",
                                "0x176FeC0DaF2f96f2d05822a84C56bfb99002eE44",
                                "0x7BACA1e69390ac9f57f9E86462a77C9898BeC066",
                            ],
                            "masterCopy": "0xd9Db270c1B5E3Bd161E8c8503c55cEABeE709552",
                            "modules": [],
                            "fallbackHandler": "0xf48f2B2d2a534e402487b3ee7C18c33Aec0Fe5e4",
                            "guard": "0x0000000000000000000000000000000000000000",
                            "version": "1.3.0",
                        }),
                    )
                elif data["invocation"]["method"] == "getTransactionConfirmations":
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content=json.dumps([
                            {
                                "owner": "0x639749b7b08aEe65039c21d8a411103C6ceBEBF0",
                                "submissionDate": "2023-04-24T09:22:33.944228Z",
                                "transactionHash": None,
                                "signature": "0x9fb2bd7fb65bfe0a88545b722912efd283d32ae83d45313be6c8772f872e309d0fed3f07ddfcf3dee72d9693f692a3106152a921afc0bd06864f61b34ffb9ebc1b",
                                "signatureType": "EOA",
                            },
                            {
                                "owner": "0x176FeC0DaF2f96f2d05822a84C56bfb99002eE44",
                                "submissionDate": "2023-04-24T13:06:11.472778Z",
                                "transactionHash": None,
                                "signature": "0x0241d9b52f8008225804a53ae5e109cab1e4f3ad1f613915394e6402387a612e3ad09769db69e855790ed7d9ddb6256a56cbc71376ecb81fa14ec708b4d8c7e71b",
                                "signatureType": "EOA",
                            },
                            {
                                "owner": "0x7BACA1e69390ac9f57f9E86462a77C9898BeC066",
                                "submissionDate": "2023-04-26T12:47:47Z",
                                "transactionHash": None,
                                "signature": "0x0000000000000000000000007baca1e69390ac9f57f9e86462a77c9898bec066000000000000000000000000000000000000000000000000000000000000000001",
                                "signatureType": "APPROVED_HASH",
                            },
                        ]),
                    )
                elif data["invocation"]["method"] == "getTokenBalances":
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content=json.dumps([
                        ]),
                    )
                elif data["invocation"]["method"] == "supportedFunctions":
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content=json.dumps([
                            "getOwner",
                            "signerAddress",
                            "deploySafe",
                            "getPendingTransactions",
                            "getSafeInfo",
                            "getTransactionConfirmations",
                            "getSafesByOwner",
                        ]),
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
                    base_url="http://localhost:8000",
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
