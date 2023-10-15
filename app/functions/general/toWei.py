function = {
  "_id": "ethers_toWei",
  "schema": {
    "name": "ethers_toWei",
    "description": "Converts the given value in Ether to its equivalent value in Wei. Returns the equivalent value in Wei as a string. Do not assume any arguments. Arguments must be passed by user.",
    "parameters": {
      "type": "object",
      "properties": {
        "eth": {
          "type": "string",
          "description": "A string representing a number in Ether"
        }
      },
      "required": ["eth"]
    }
  },
  "description": "Convert the value in {eth} Ether to its equivalent value in Wei.",
  "invocation": {
    "uri": "wrapscan.io/polywrap/ethers-utils@1.0.1",
    "method": "toWei",
    "args": "{{ \"eth\": \"{eth}\" }}"
  }
}
