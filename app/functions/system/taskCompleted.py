function = {
  "_id": "system_taskCompleted",
  "schema": {
    "name": "system_taskCompleted",
    "description": "This function should only be called once the given task is completed or when you can't do the task.\nYou should use result of the executed functions and metadata to write message that user would need to confirm the task has been achieved.\nAfter invoking this function, You must wait for a new task from the user.",
    "parameters": {
        "type": "object",
        "properties": {
            "message": {
                "type": "string",
                "minLength": 1,
                "description": "The message that you want to send to the user upon completion of the task.\nThis message must be written in a way that the user can confirm that the task has been completed."
            }
        },
        "required": ["message"]
    }
  },
  "description": "Agent: {message}",
  "invocation": {
    "uri": "wrap://wrapscan.io/polywrap/system/taskCompleted@1.0",
    "method": "taskCompleted",
    "args": "{{ \"message\": \"{message}\" }}"
  }
}
