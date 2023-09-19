import os
from motor.motor_asyncio import AsyncIOMotorClient

client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
db = client["unblock_agent_db"]

chat_collection = db["chats"]
functions_collection = db["functions"]
