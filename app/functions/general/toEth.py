function = {
  "_id": "ethers_toEth",
  "schema": {
    "name": "ethers_toEth",
    "description": "Converts the given value in Wei to its equivalent value in Ether. Returns the equivalent value in Ether as a string. Do not assume any arguments. Arguments must be passed by user.",
    "parameters": {
      "type": "object",
      "properties": {
        "wei": {
          "type": "string",
          "description": "A string representing a number in Wei"
        }
      },
      "required": ["wei"]
    }
  },
  "description": "Converts the value in {wei} Wei to its equivalent value in Ether.",
  "invocation": {
    "uri": "wrapscan.io/polywrap/ethers-utils@1.0.1",
    "method": "toEth",
    "args": "{{ \"wei\": \"{wei}\" }}"
  }
}
