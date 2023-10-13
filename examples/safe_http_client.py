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
                if data["invocation"]["method"] in ["getSignerAddress"]:
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content="0x4675C7e5BaAFBFFbca748158bEcBA61ef3b0a263",
                    )
                elif data["invocation"]["method"] in ["getDomainInfo"]:
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content=json.dumps(
                            {
                                "id": "0xee6c4522aab0003e8d14cd40a6af439055fd2577951148c14b6cea9a53475835",
                                "name": "vitalik.eth",
                                "labelName": "vitalik",
                                "labelhash": "0xaf2caa1c2ca1d027f1ac823b529d0a67cd144264b2789fa2ea4d63a67c7103cc",
                                "owner": {
                                    "id": "0xd8da6bf26964af9d7eed9e03e53415d37aa96045"
                                },
                                "resolvedAddress": {
                                    "id": "0xd8da6bf26964af9d7eed9e03e53415d37aa96045"
                                },
                                "resolver": {
                                    "id": "0x4976fb03c32e5b8cfe2b6ccb31c09ba78ebaba41-0xee6c4522aab0003e8d14cd40a6af439055fd2577951148c14b6cea9a53475835"
                                },
                            }
                        ),
                    )
                elif data["invocation"]["method"] == "getSafesByOwner":
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content="{\"safes\":[\"0x164cb3676F4A465403F269730F0B4dE0E9D47298\",\"0x4449C2916e53F6337Fd8c776F95e37e9365F005a\",\"0x77256aA4CC49649E2Ed1c91F66738e969821ee32\",\"0x7854e996686edca87933F3247E74353D8691bada\",\"0x039f3f7ae9a75Aa454c6200d0A2BE802cFd6795C\",\"0x57236ec948125F3c28642b05eDB7a775135703c6\",\"0x2C618aC0e882570c7e65B2aFDAeC5b98B5444387\",\"0xEB25f75AaD45e74fBD7E5aBd3467EC06D1Aa82F6\",\"0x94202F9ee83d21D243335a61e79b0A19eB308150\",\"0x0607ba4a93460c1f21ABCAb3B731E5189A93635c\",\"0x2678e9537EF09Ac8CAeeC72E9c044bb6D79E437D\",\"0xabff5AfD405176DD22803501fF3d9Bc0adc19004\",\"0x79E490c4933e508BA2f33Ac7b55aF6e637E572Fe\",\"0xaaeEB0d44a66B7da5ed50e804a022fD364Cc8d5A\",\"0xFB1248819b82928230b2861166c8A55eb9D1d8ea\",\"0xfFEDEdBD28E4C0dbE0A1c51058A6f10132F3A686\",\"0x8e160C8E949967D6B797CdF2A2F38f6344a5C95f\",\"0x9af3b5e801B5736e8c8935D60a92Cd89Fad71DF2\",\"0xB36082ba6c35490D1E167CC6Dd5ad20884A21Afb\",\"0xB6E8983C255c3FAF2a739901da358d8F8983CCD9\",\"0x6928Dcc6366Aa661d5cABb53205D10d20b794c5B\",\"0xC3006DA4751eC51Ca7e7BDd2D271936944324818\",\"0x220866B1A2219f40e72f5c628B65D54268cA3A9D\",\"0x59A6a7932353fc742648FFbaF2A505BbdAEB5a2C\",\"0xA06C2B67e7435cE25a5969e49983ec3304D8e787\",\"0x989C7C60F603Ec8ebEf925Ba4917270B35593353\",\"0x9C0b64dF36e9fCE685609f63E09ce37625393D74\",\"0xF7669e198C7fC4085131116014CEF2174bdB9B64\",\"0xe2E089e25beBdB65682a2e7362063f3017416e47\",\"0x0B19E087493a6EC31661470bd9bA6C49873E97f0\",\"0xf20784fB0047fE897919B1cd4264daD364C9D5a3\"]},\"error\":null}",
                    )
                # Use this function to transfer or send wei/gwei/ether from a safe address to someone without any data.
                elif data["invocation"]["method"] == "createTransaction":
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content=json.dumps(
                            {
                                "safeTxHash": "0xb0c589d7f025ad8396d5127bbf48c141fed2e42a5c857b42cf3d12aac2d692ee"
                            }
                        ),
                    )
                elif data["invocation"]["method"] == "signTransaction":
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content=json.dumps(
                            {
                                "signature": "0x827abc893892bcddd29293388370000928928bce9289298389ddff7292ff0229"
                            }
                        ),
                    )
                elif data["invocation"]["method"] == "executeTransaction":
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content=json.dumps(
                            {
                                "txHash": "0xf1014ca9760db3a4bb75d187606c4af0563576231a2b2d30be2aaea19321506a"
                            }
                        ),
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
                        content=json.dumps(
                            [
                                "0xa2f696efe1c78c823ca52e1badbaaecc95e61708913423e9baf647ebad791cd7",
                                "0xb0c589d7f025ad8396d5127bbf48c141fed2e42a5c857b42cf3d12aac2d692ee",
                                "0xf1014ca9760db3a4bb75d187606c4af0563576231a2b2d30be2aaea19321506a",
                            ]
                        ),
                    )
                elif data["invocation"]["method"] == "getSafeInfo":
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content=json.dumps(
                            {
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
                            }
                        ),
                    )
                elif data["invocation"]["method"] == "getTransactionConfirmations":
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content=json.dumps(
                            [
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
                            ]
                        ),
                    )
                elif data["invocation"]["method"] == "getTokenBalances":
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content=json.dumps([]),
                    )
                elif data["invocation"]["method"] == "supportedFunctions":
                    result = dict(
                        type="FUNCTION",
                        function_name=data["functionName"],
                        content=json.dumps(
                            [
                                "getOwner",
                                "signerAddress",
                                "deploySafe",
                                "getPendingTransactions",
                                "getSafeInfo",
                                "getTransactionConfirmations",
                                "getSafesByOwner",
                            ]
                        ),
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
