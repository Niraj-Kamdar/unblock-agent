function = {
  "_id": "ens_getDomainInfo",
  "schema": {
    "name": "ens_getDomainInfo",
    "description": "Get the informations about the ens domain. It includes the owner, resolver, domain name, and the address associated with the domain (resolved address). Use this function when you need to get info about an ENS domain. ENS domain ends with `.eth` suffix.",
    "parameters": {
        "type": "object",
        "properties": {
            "domain": {
                "type": "string",
                "pattern": "^(.*\\.eth)$",
                "description": "The ENS name, Ex: alice.eth"
            }
        },
        "required": ["domain"]
    }
  },
  "description": "Get the info about {domain}.",
  "invocation": {
    "uri": "wrap://wrapscan.io/polywrap/ens-plugin@1.0",
    "method": "getDomainInfo",
    "args": "{{ \"domain\": \"{domain}\" }}"
  }
}
