function = {
  "_id": "covalent_getTokenBalances",
  "schema": {
    "name": "covalent_getTokenBalances",
    "description": "Get token balances for a specific account. This function can be used to get balance, portfolio, token balances or total assets of a person on the blockchain. Note: token balances are always in correct decimals format with maximum precision. Do not convert them to Wei or Ether.",
    "parameters": {
      "type": "object",
      "properties": {
        "accountAddress": {
          "type": "string",
          "pattern": "^0x[a-fA-F0-9]{40}$",
          "description": "The Ethereum address of the account for which token balances are requested."
        }
      },
      "required": ["accountAddress"]
    }
  },
  "requireSign": True,
  "description": "Get token balances for the Ethereum address {accountAddress}.",
  "invocation": {
    "uri": "wrapscan.io/polywrap/covalent@1.0",
    "method": "getTokenBalances",
    "args": "{{ \"accountAddress\": \"{accountAddress}\" }}"
  }
}
