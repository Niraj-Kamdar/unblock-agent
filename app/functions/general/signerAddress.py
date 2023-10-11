from typing import Any


function: dict[str, Any] = {
    "_id": "ethers_getSignerAddress",
    "schema": {
        "name": "ethers_getSignerAddress",
        "description": "Get the address of the connected signer",
        "parameters": {"type": "object", "properties": {}, "required": []},
    },
    "description": "Get the address of the connected signer. It can be used to get ethereum address of the user.",
    "invocation": {
        "uri": "wrap://wrapscan.io/polywrap/ethers@1.1.1",
        "method": "getSignerAddress",
        "args": "{{}}",
    },
}