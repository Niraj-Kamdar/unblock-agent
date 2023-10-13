function = {
  "_id": "safe_getTransactionConfirmations",
  "schema": {
    "name": "safe_getTransactionConfirmations",
    "description": "Returns the list of confirmations for a given Safe transaction. It can be used to get list of confirmations for a pending transaction on a safe.",
    "parameters": {
      "type": "object",
      "properties": {
        "safeTxHash": {
          "type": "string",
          "description": "The hash of the Safe transaction.",
          "pattern": "^0x[a-fA-F0-9]{40}$"
        }
      },
      "required": ["safeTxHash"]
    }
  },
  "requireSign": True,
  "description": "Get the list of confirmations for the safe transaction: {safeTxHash}.",
  "invocation": {
    "uri": "plugin/safe-api-kit@1.0",
    "method": "getTransactionConfirmations",
    "args": "{{\"safeTxHash\": \"{safeTxHash}\"}}"
  }
}
