function = {
  "_id": "safe_addOwner",
  "schema": {
    "name": "safe_addOwner",
    "description": "Adds an owner to a specified safe and updates the threshold for the safe. Use this function when user wants to add a new owner to the safe.",
    "parameters": {
      "type": "object",
      "properties": {
        "safeAddress": {
          "type": "string",
          "description": "The address of the safe to which the new owner will be added.",
          "pattern": "^(0x[a-fA-F0-9]{40})$"
        },
        "ownerAddress": {
          "type": "string",
          "description": "The address of the new owner to be added to the safe.",
          "pattern": "^(0x[a-fA-F0-9]{40})$"
        },
        "newThreshold": {
          "type": "integer",
          "description": "The new threshold value to be set for the safe after adding the new owner.",
          "minimum": 1
        }
      },
      "required": ["safeAddress", "ownerAddress", "newThreshold"]
    }
  },
  "requireSign": True,
  "description": "Add {ownerAddress} as owner of {safeAddress} and update threshold to {newThreshold}.",
  "invocation": {
    "uri": "plugin/safe-tx-plugin@1.0",
    "method": "addOwner",
    "args": "{{ \"safeAddress\": \"{safeAddress}\", \"ownerAddress\": \"{ownerAddress}\", \"newThreshold\": {newThreshold} }}"
  }
}
