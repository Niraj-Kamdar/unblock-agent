function = {
  "_id": "ens_getOwner",
  "schema": {
    "name": "ens_getOwner",
    "description": "Get the owner of an ENS name.",
    "parameters": {
        "type": "object",
        "properties": {
            "ens": {
                "type": "string",
                "pattern": "^(.*\\.eth)$",
                "description": "The ENS name, Ex: alice.eth"
            }
        },
        "required": ["ens"]
    }
  },
  "description": "Get the owner of {ens}.",
  "invocation": {
    "uri": "wrap://wrapscan.io/polywrap/ens@1.0",
    "method": "getOwner",
    "args": "{{ \"domain\": \"{ens}\" }}"
  }
}
