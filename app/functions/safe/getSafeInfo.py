function = {
  "_id": "safe_getSafeInfo",
  "schema": {
    "name": "safe_getSafeInfo",
    "description": "Returns the information and configuration of the provided Safe address. Returns the address, nonce, threshold, owners, modules, version, etc of the given safe.",
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
  "description": "Get the info and configuration of {safeAddress} safe.",
  "invocation": {
    "uri": "plugin/safe-api-kit",
    "method": "getSafeInfo",
    "args": "{{ \"safeAddress\": \"{safeAddress}\" }}"
  }
}
