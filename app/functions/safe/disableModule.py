function = {
  "_id": "safe_disableModule",
  "schema": {
    "name": "safe_disableModule",
    "description": "Disables a module for a specified safe.",
    "parameters": {
      "type": "object",
      "properties": {
        "safeAddress": {
          "type": "string",
          "description": "The address of the safe for which the module will be disabled.",
          "pattern": "^(0x[a-fA-F0-9]{40})$"
        },
        "moduleAddress": {
          "type": "string",
          "description": "The address of the module to be disabled for the safe.",
          "pattern": "^(0x[a-fA-F0-9]{40})$"
        }
      },
      "required": ["safeAddress", "moduleAddress"]
    }
  },
  "description": "Disable {moduleAddress} module for {safeAddress} safe.",
  "invocation": {
    "uri": "plugin/safe-tx-plugin@1.0",
    "method": "disableModule",
    "args": "{{ \"safeAddress\": \"{safeAddress}\", \"moduleAddress\": \"{moduleAddress}\" }}"
  }
}
