function = {
  "_id": "safe_removeOwner",
  "schema": {
    "name": "safe_removeOwner",
    "description": "Removes an owner from a specified safe and updates the threshold for the safe.",
    "parameters": {
      "type": "object",
      "properties": {
        "safeAddress": {
          "type": "string",
          "description": "The address of the safe from which the owner will be removed.",
          "pattern": "^(0x[a-fA-F0-9]{40})$"
        },
        "ownerAddress": {
          "type": "string",
          "description": "The address of the owner to be removed from the safe.",
          "pattern": "^(0x[a-fA-F0-9]{40})$"
        },
        "newThreshold": {
          "type": "integer",
          "description": "The new threshold value to be set for the safe after removing the owner."
        }
      },
      "required": ["safeAddress", "ownerAddress", "newThreshold"]
    }
  },
  "requireSign": True,
  "description": "Remove {ownerAddress} as owner of {safeAddress} and update threshold to {newThreshold}.",
  "invocation": {
    "uri": "plugin/safe-tx-plugin@1.0",
    "method": "removeOwner",
    "args": "{{ \"safeAddress\": \"{safeAddress}\", \"ownerAddress\": \"{ownerAddress}\", \"newThreshold\": {newThreshold} }}"
  }
}
