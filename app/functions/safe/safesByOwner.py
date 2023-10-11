function = {
  "_id": "safe_getSafesByOwner",
  "schema": {
    "name": "safe_getSafesByOwner",
    "description": "Returns the list of Safes where the address provided is an owner.",
    "parameters": {
      "type": "object",
      "properties": {
        "ownerAddress": {
          "type": "string",
          "description": "The owner's ethereum address.",
          "pattern": "^0x[a-fA-F0-9]{40}$"
        }
      },
      "required": ["ownerAddress"]
    }
  },
  "description": "Returns the list of Safes where {ownerAddress} is an owner.",
  "invocation": {
    "uri": "plugin/safe-api-kit",
    "method": "getSafesByOwner",
    "args": "{{\"ownerAddress\": \"{ownerAddress}\"}}"
  }
}
