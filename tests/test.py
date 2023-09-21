# test_main.py

import json
import contextlib
import secrets

import websockets
import asyncio

async def test_websocket():
    chat_id = secrets.token_hex(16)
    async with websockets.connect(f"wss://unblock-agent.fly.dev/chats/{chat_id}?api-key=923adjhb-288cbjSudhuido-828bchbcj", subprotocols=[chat_id]) as websocket:
        # await websocket.send("Send 5 ether to vitalik.eth")
        with contextlib.suppress(websockets.ConnectionClosed):
            await websocket.send("Send 5 ether to vitalik.eth")
            while True:
                data = json.loads(await websocket.recv())
                print(data)
                if data.get("content") and data["content"] == "DONE":
                    break
                if data.get("error"):
                    await websocket.send("IGNORE")
                    continue
                if data.get("invocation"):
                    if data["content"]["method"] in ["getOwner", "getAddress"]:
                        await websocket.send("0xaddr81784836247647474")
                    elif data["content"]["method"] == "getBalance":
                        await websocket.send("0.373892")
                    elif data["content"]["method"] == "sendTransaction":
                        await websocket.send("0xtrans81784836247647827428474894474")
                    continue


asyncio.run(test_websocket())