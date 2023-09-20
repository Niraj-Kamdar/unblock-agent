from motor.motor_asyncio import AsyncIOMotorClient

from .constants import MONGO_URL

client = AsyncIOMotorClient(MONGO_URL)
db = client["unblock_agent_db"]

chat_collection = db["chats"]
functions_collection = db["functions"]
