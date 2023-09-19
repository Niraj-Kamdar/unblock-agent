import json
import os
import asyncio
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import ReplaceOne
from dotenv import load_dotenv

load_dotenv()  # take environment variables from .env.


client = AsyncIOMotorClient(os.getenv("MONGO_URL"))
db = client["unblock_agent_db"]


functions_collection = db["functions"]


async def batch_upsert(collection, documents):
    # Create the list of ReplaceOne operations with upsert=True
    operations = [ReplaceOne({"_id": doc["_id"]}, doc, upsert=True) for doc in documents]

    # Perform the batch upsert operation
    result = await collection.bulk_write(operations)

    print(f"Modified documents: {result.modified_count}")
    print(f"Upserted documents: {len(result.upserted_ids)}")

    # Close the MongoDB connection
    client.close()


def load_functions():
    functions_path = os.path.join(os.path.dirname(__file__), "functions")
    functions = []

    for root, _, files in os.walk(functions_path):
        for file in files:
            if file.endswith(".json"):
                json_file_path = os.path.join(root, file)
                with open(json_file_path, "r") as json_file:
                    data = json.load(json_file)
                    functions.append(data)

    return functions


if __name__ == "__main__":
    functions = load_functions()
    asyncio.run(batch_upsert(functions_collection, functions))
