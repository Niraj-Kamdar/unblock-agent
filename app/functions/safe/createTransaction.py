function = {
  "_id": "safe_createTransaction",
  "schema": {
    "name": "safe_createTransaction",
    "description": "Creates a new transaction for the specified safe address. This function can be used to transfer ether to someone or call a contract function with encoded data. If the transaction is to transfer ether, the data field should be 0x0.",
    "parameters": {
      "type": "object",
      "properties": {
        "safeAddress": {
          "type": "string",
          "description": "The address of the safe where the transaction is to be created.",
          "pattern": "^(0x[a-fA-F0-9]{40})$"
        },
        "to": {
          "type": "string",
          "description": "The recipient address of the transaction.",
          "pattern": "^(0x[a-fA-F0-9]{40})$"
        },
        "data": {
          "type": "string",
          "description": "The transaction data.",
          "pattern": "^0x[a-fA-F0-9]+$"
        },
        "value": {
          "type": "string",
          "description": "The value to be transferred with the transaction.",
          "minLength": 1
        }
      },
      "required": ["safeAddress", "to", "data", "value"]
    }
  },
  "requireSign": True,
  "description": "Create a transaction to send {value} wei to {to} with given data from {safeAddress} safe.",
  "invocation": {
    "uri": "plugin/safe-tx-plugin@1.0",
    "method": "createTransaction",
    "args": "{{ \"safeAddress\": \"{safeAddress}\", \"to\": \"{to}\", \"data\": \"{data}\", \"value\": \"{value}\" }}"
  }
}
