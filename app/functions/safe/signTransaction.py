function = {
  "_id": "safe_signTransaction",
  "schema": {
    "name": "safe_signTransaction",
    "description": "Signs a specified transaction of the given safe address.",
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
          "description": "The safe transaction hash to be signed.",
          "pattern": "^0x[a-fA-F0-9]*$"
        }
      },
      "required": ["safeAddress", "safeTxHash"]
    }
  },
  "requireSign": True,
  "description": "Sign {safeTxHash} transaction of {safeAddress} safe.",
  "invocation": {
    "uri": "plugin/safe-tx-plugin@1.0",
    "method": "signTransaction",
    "args": "{{ \"safeAddress\": \"{safeAddress}\", \"safeTxHash\": \"{safeTxHash}\" }}"
  }
}
