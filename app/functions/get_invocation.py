
import json
from typing import Any

from .get_openai_functions import get_functions
from ..schemas import InvocationContent
import jsonschema


def get_invocation_content(
    function_name: str,
    function_parameters: dict[str, Any],
) -> InvocationContent:
    functions = get_functions()
    function =  functions.get(function_name)
    if not function:
        raise ValueError(f"Function {function_name} not found")

    if function["schema"].get("parameters"):
        parameters_schema = function["schema"]["parameters"]
        print(function_parameters)
        print(parameters_schema)
        jsonschema.validate(function_parameters, parameters_schema)

    invocation = json.loads(json.dumps(function["invocation"]))
    from pprint import pprint
    print(invocation["args"].format(**function_parameters))
    invocation["args"] = json.loads(invocation["args"].format(**function_parameters))
    description = function["description"].format(**function_parameters)
    require_sign = function.get("requireSign", False)

    return InvocationContent.model_validate(
        {
            "function_name": function_name,
            "invocation": invocation,
            "description": description,
            "require_sign": require_sign,
        }
    )
