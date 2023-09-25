import json
import jsonschema
from typing import Any

from motor.core import AgnosticCollection

async def load_functions(functions_collection: AgnosticCollection, ids: list[str]) -> list[Any]:
    # Fetch documents by their IDs
    cursor = functions_collection.find({"_id": {"$in": ids}})
    return await cursor.to_list(length=None)  # type: ignore


async def load_functions_by_namespace(functions_collection: AgnosticCollection, namespace: str) -> list[Any]:
    # Use a regex to find documents with _id starting with 'prefix_'
    cursor = functions_collection.find({"_id": {"$regex": f"^{namespace}_"}})
    return await cursor.to_list(length=None)  # type: ignore


async def get_invocation(
    functions_collection: AgnosticCollection, function_name: str, function_parameters: dict[str, Any]
) -> dict[str, Any]:
    function = await functions_collection.find_one({"_id": function_name})
    if not function:
        raise ValueError(f"Function {function_name} not found")

    if function["schema"].get("parameters"):
        parameters_schema = function["schema"]["parameters"]
        jsonschema.validate(function_parameters, parameters_schema)

    invocation = function["invocation"]
    invocation["args"] = json.loads(invocation["args"].format(**function_parameters))
    return invocation

