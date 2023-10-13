function = {
  "_id": "safe_changeThreshold",
  "schema": {
    "name": "safe_changeThreshold",
    "description": "Updates the threshold for a specified safe. Threshold is number of signatures required for execution of a transaction.",
    "parameters": {
      "type": "object",
      "properties": {
        "safeAddress": {
          "type": "string",
          "description": "The address of the safe for which the threshold will be updated.",
          "pattern": "^(0x[a-fA-F0-9]{40})$"
        },
        "newThreshold": {
          "type": "integer",
          "description": "The new threshold value to be set for the safe."
        }
      },
      "required": ["safeAddress", "newThreshold"]
    }
  },
  "requireSign": True,
  "description": "Update the threshold of {safeAddress} to {newThreshold}.",
  "invocation": {
    "uri": "plugin/safe-tx-plugin@1.0",
    "method": "changeThreshold",
    "args": "{{ \"safeAddress\": \"{safeAddress}\", \"newThreshold\": {newThreshold} }}"
  }
}
