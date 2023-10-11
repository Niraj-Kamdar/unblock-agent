function = {
  "_id": "safe_getPendingTransactions",
  "schema": {
    "name": "safe_getPendingTransactions",
    "description": "Returns the list of multi-signature transactions that are waiting for the confirmation of the Safe owners.",
    "parameters": {
      "type": "object",
      "properties": {
        "safeAddress": {
          "type": "string",
          "description": "The Safe address.",
          "pattern": "^0x[a-fA-F0-9]{40}$"
        }
      },
      "required": ["safeAddress"]
    }
  },
  "description": "Get pending transactions for {safeAddress} safe",
  "invocation": {
    "uri": "plugin/safe-api-kit@1.0",
    "method": "getPendingTransactions",
    "args": "{{\"safeAddress\": \"{safeAddress}\"}}"
  }
}
