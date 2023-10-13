function = {
  "_id": "safe_getPendingTransactions",
  "schema": {
    "name": "safe_getPendingTransactions",
    "description": "Returns the list of multi-signature transactions that aren't executed yet.",
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
  "requireSign": True,
  "description": "Get pending transactions for {safeAddress} safe",
  "invocation": {
    "uri": "plugin/safe-api-kit@1.0",
    "method": "getPendingTransactions",
    "args": "{{\"safeAddress\": \"{safeAddress}\"}}"
  }
}
