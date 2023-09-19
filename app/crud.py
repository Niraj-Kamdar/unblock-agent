from .database import functions_collection


async def load_functions(ids):
    # Fetch documents by their IDs
    cursor = functions_collection.find({"id": {"$in": ids}})
    return await cursor.to_list(length=None)
