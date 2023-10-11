function = {
  "_id": "system_askQuestion",
  "schema": {
    "name": "system_askQuestion",
    "description": "This function can be used to ask any question to the user.\nUse this function if the initial prompt given by user isn't complete or lacks clarity to make informed decision.",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "minLength": 1,
                "description": "Question you want to ask to the user."
            }
        },
        "required": ["question"]
    }
  },
  "description": "Agent: {question}",
  "invocation": {
    "uri": "wrap://wrapscan.io/polywrap/system/askQuestion@1.0",
    "method": "askQuestion",
    "args": "{{ \"question\": {json_question} }}"
  }
}
