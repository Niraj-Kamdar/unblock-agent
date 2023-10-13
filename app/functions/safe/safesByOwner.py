function = {
  "_id": "safe_getSafesByOwner",
  "schema": {
    "name": "safe_getSafesByOwner",
    "description": "Returns the list of Safes where the address provided is an owner(signer). <Note: Owner or signer can be said to be part of the safe>.",
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
  "requireSign": True,
  "description": "Returns the list of Safes where {ownerAddress} is an owner.",
  "invocation": {
    "uri": "plugin/safe-api-kit@1.0",
    "method": "getSafesByOwner",
    "args": "{{\"ownerAddress\": \"{ownerAddress}\"}}"
  }
}
