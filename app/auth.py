from fastapi import HTTPException, Security, WebSocket, status
from fastapi.security import APIKeyHeader, APIKeyQuery

API_KEYS = {"923adjhb-288cbjSudhuido-828bchbcj"}

from urllib.parse import parse_qs


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
    query_string = websocket.scope.get("query_string")
    if not query_string:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key",
        )

    query_params = parse_qs(query_string.decode())
    api_key_query = query_params.get("api-key", [None])[0]

    if api_key_query and api_key_query in API_KEYS:
        return api_key_query
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid API Key",
    )


api_key_query = APIKeyQuery(name="api-key", auto_error=False)
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def get_api_key(
    api_key_query: str = Security(api_key_query),
    api_key_header: str = Security(api_key_header),
) -> str:
    """Retrieve and validate an API key from the query parameters or HTTP header.

    Args:
        api_key_query: The API key passed as a query parameter.
        api_key_header: The API key passed in the HTTP header.

    Returns:
        The validated API key.

    Raises:
        HTTPException: If the API key is invalid or missing.
    """
    if api_key_query in API_KEYS:
        return api_key_query
    if api_key_header in API_KEYS:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing API Key",
    )
