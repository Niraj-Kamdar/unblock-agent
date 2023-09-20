from fastapi import HTTPException, WebSocket, status

API_KEYS = {"923adjhb-288cbjSudhuido-828bchbcj"}

from urllib.parse import parse_qs

# ...


def validate_api_key(
    websocket: WebSocket,
) -> str:
    """
    Retrieve and validate an API key from the query parameters.

    Args:
        websocket (WebSocket): The current websocket connection.

    Returns:
        str: The validated API key.

    Raises:
        HTTPException: If the API key is invalid or missing.
    """

    # Parse the query string from the websocket scope
    query_string = websocket.scope.get("query_string").decode()
    query_params = parse_qs(query_string)
    api_key_query = query_params.get("api-key", [None])[0]

    if api_key_query and api_key_query in API_KEYS:
        return api_key_query
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
