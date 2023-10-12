function = {
  "_id": "safe_enableModule",
  "schema": {
    "name": "safe_enableModule",
    "description": "Enables a module for a specified safe.",
    "parameters": {
      "type": "object",
      "properties": {
        "safeAddress": {
          "type": "string",
          "description": "The address of the safe for which the module will be enabled.",
          "pattern": "^(0x[a-fA-F0-9]{40})$"
        },
        "moduleAddress": {
          "type": "string",
          "description": "The address of the module to be enabled for the safe.",
          "pattern": "^(0x[a-fA-F0-9]{40})$"
        }
      },
      "required": ["safeAddress", "moduleAddress"]
    }
  },
  "description": "Enable {moduleAddress} module for {safeAddress} safe.",
  "invocation": {
    "uri": "plugin/safe-tx-plugin@1.0",
    "method": "enableModule",
    "args": "{{ \"safeAddress\": \"{safeAddress}\", \"moduleAddress\": \"{moduleAddress}\" }}"
  }
}
