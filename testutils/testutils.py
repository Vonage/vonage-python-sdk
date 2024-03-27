from os.path import dirname, join
from typing import Literal

import responses
from pydantic import validate_call


def _load_mock_data(caller_file_path: str, mock_path: str):
    with open(join(dirname(caller_file_path), 'data', mock_path)) as file:
        return file.read()


def _filter_none_values(data: dict) -> dict:
    return {k: v for (k, v) in data.items() if v is not None}


@validate_call
def build_response(
    file_path: str,
    method: Literal['GET', 'POST', 'PATCH', 'DELETE'],
    url: str,
    mock_path: str = None,
    status_code: int = 200,
    content_type: str = 'application/json',
    match: list = None,
):
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
