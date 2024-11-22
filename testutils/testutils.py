from os.path import dirname, join
from typing import Literal

import responses
from pydantic import validate_call


def _load_mock_data(caller_file_path: str, mock_path: str):
    """Load mock data from a file."""

    try:
        with open(join(dirname(caller_file_path), 'data', mock_path)) as file:
            return file.read()
    except UnicodeDecodeError:
        with open(join(dirname(caller_file_path), 'data', mock_path), 'rb') as file:
            return file.read()


def _filter_none_values(data: dict) -> dict:
    """Filter out None values from a dictionary."""

    return {k: v for (k, v) in data.items() if v is not None}


@validate_call
def build_response(
    file_path: str,
    method: Literal['GET', 'POST', 'PATCH', 'PUT', 'DELETE'],
    url: str,
    mock_path: str = None,
    status_code: int = 200,
    content_type: str = 'application/json',
    match: list = None,
):
    """Build a response for a mock request.

    Args:
        file_path (str): The path to the file calling this function.
        method (Literal['GET', 'POST', 'PATCH', 'PUT', 'DELETE']): The HTTP method.
        url (str): The URL to match.
        mock_path (str, optional): The path to the mock data file.
        status_code (int, optional): The status code to return.
        content_type (str, optional): The content type to return.
        match (list, optional): The match parameters.
    """

    body = _load_mock_data(file_path, mock_path) if mock_path else None
    responses.add(
        **_filter_none_values(
            {
                'method': method,
                'url': url,
                'body': body,
                'status': status_code,
                'content_type': content_type,
                'match': match,
            }
        )
    )
