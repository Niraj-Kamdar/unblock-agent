function = {
  "_id": "covalent_getTokenTransfers",
  "schema": {
    "name": "covalent_getTokenTransfers",
    "description": "Get token transfers for a specific ethereum account and token. Returns historical token transfers for a given ethereum address and a token address.",
    "parameters": {
      "type": "object",
      "properties": {
        "accountAddress": {
          "type": "string",
          "pattern": "^0x[a-fA-F0-9]{40}$",
          "description": "The Ethereum address of the account for which token transfers are requested."
        },
        "tokenAddress": {
          "type": "string",
          "pattern": "^0x[a-fA-F0-9]{40}$",
          "description": "The Ethereum address of the token for which transfers are requested."
        },
        "options": {
          "type": "object",
          "properties": {
            "pagination": {
              "type": "object",
              "properties": {
                "page": {
                  "type": "integer"
                },
                "perPage": {
                  "type": "integer"
                }
              },
              "required": ["page", "perPage"]
            },
            "blockRange": {
              "type": "object",
              "properties": {
                "startBlock": {
                  "type": "integer"
                },
                "endBlock": {
                  "type": "integer"
                }
              }
            }
          }
        }
      },
      "required": ["accountAddress", "tokenAddress"]
    }
  },
  "requireSign": True,
  "description": "Get token transfers for the Ethereum address {accountAddress} and token address {tokenAddress}.",
  "invocation": {
    "uri": "wrapscan.io/polywrap/covalent@1.0",
    "method": "getTokenTransfers",
    "args": "{{\"accountAddress\": \"{ accountAddress }\", \"tokenAddress\": \"{ tokenAddress }\", \"options\": { options } }}"
  }
}
