function = {
  "_id": "safe_createTransaction",
  "schema": {
    "name": "safe_createTransaction",
    "description": "Creates a new transaction for the specified safe address. This function can be used to transfer ether (in Wei unit) to someone or call a contract function with encoded data. If the transaction is to transfer ether (in Wei unit), the data field should be 0x00.",
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
          "pattern": "^0x[a-fA-F0-9]+$",
          "minLength": 4
        },
        "value": {
          "type": "integer",
          "description": "The value to be transferred with the transaction in Wei. if specified in Ether, convert it to Wei before passing it to this function. Use ethers_toWei function to convert Ether to Wei.",
          "minimum": 0
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
