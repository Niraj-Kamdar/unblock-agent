function = {
  "_id": "safe_deploySafe",
  "schema": {
    "name": "safe_deploySafe",
    "description": "Deploys a new Safe smart contract. Safe is a multisig account on ethereum.",
    "parameters": {
      "type": "object",
      "properties": {
        "owners": {
          "type": "array",
          "items": {
            "type": "string",
            "pattern": "^0x[a-fA-F0-9]{40}$"
          }
        },
        "threshold": {
          "type": "integer",
          "minimum": 1
        }
      },
      "required": ["owners", "threshold"]
    }
  },
  "description": "Deploy a new safe with the {owners} as owners and {threshold} threshold.",
  "invocation": {
    "uri": "wrapscan.io/polywrap/protocol-kit@0.1.0",
    "method": "deploySafe",
    "args": "{{\"safeAccountConfig\": {{\"owners\": {owners}, \"threshold\": {threshold} }} }}"
  }
}
