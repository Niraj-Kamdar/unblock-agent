from typing import Any


function: dict[str, Any] = {
    "_id": "system_supportedFunctions",
    "schema": {
        "name": "system_supportedFunctions",
        "description": "Returns all the functions the AI supports.",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    "description": "Fetch Supported Functions",
    "invocation": {
        "uri": "wrap://wrapscan.io/polywrap/system/supportedFunctions@1.0",
        "method": "supportedFunctions",
        "args": "{{}}",
    },
}