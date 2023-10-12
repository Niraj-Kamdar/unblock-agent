function = {
  "_id": "safe_executeTransaction",
  "schema": {
    "name": "safe_executeTransaction",
    "description": "Executes a specified transaction for the given safe address using the provided transaction hash.",
    "parameters": {
      "type": "object",
      "properties": {
        "safeAddress": {
          "type": "string",
          "description": "The address of the safe related to the transaction.",
          "pattern": "^(0x[a-fA-F0-9]{40})$"
        },
        "safeTxHash": {
          "type": "string",
          "description": "The unique hash of the transaction to be executed.",
          "pattern": "^0x[a-fA-F0-9]*$"
        }
      },
      "required": ["safeAddress", "safeTxHash"]
    }
  },
  "description": "Execute {safeTxHash} transaction of {safeAddress} safe.",
  "invocation": {
    "uri": "plugin/safe-tx-plugin@1.0",
    "method": "executeTransaction",
    "args": "{{ \"safeAddress\": \"{safeAddress}\", \"safeTxHash\": \"{safeTxHash}\" }}"
  }
}
