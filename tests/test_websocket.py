import json
from fastapi.testclient import TestClient
import contextlib
import secrets

import websockets

from app.main import app  # Import the FastAPI instance from your application

client = TestClient(app)

def test_websocket():
    chat_id = secrets.token_hex(16)
    with client.websocket_connect(f"/chats/{chat_id}?api-key=923adjhb-288cbjSudhuido-828bchbcj", chat_id) as websocket:
        with contextlib.suppress(websockets.ConnectionClosed):
            websocket.send_text("Send 5 ether to vitalik.eth")
            while True:
                data = json.loads(websocket.receive_text())
                if data.get("content") and data["content"] == "DONE":
                    break
                if data.get("error"):
                    websocket.send_text("IGNORE")
                    continue
                if data.get("invocation"):
                    if data["content"]["method"] in ["getOwner", "getAddress"]:
                        websocket.send_text("0xaddr81784836247647474")
                    elif data["content"]["method"] == "getBalance":
                        websocket.send_text("0.373892")
                    elif data["content"]["method"] == "sendTransaction":
                        websocket.send_text("0xtrans81784836247647827428474894474")
                    continue
