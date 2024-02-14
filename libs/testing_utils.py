from os.path import dirname, join
from typing import Literal

import responses
from pydantic import validate_call


def _load_mock_data(caller_file_path: str, mock_path: str):
    with open(join(dirname(caller_file_path), 'data', mock_path)) as file:
        return file.read()


@validate_call
def build_response(
    file_path: str,
    method: Literal['GET', 'POST'],
    url: str,
    mock_path: str = None,
    status_code: int = 200,
    content_type: str = 'application/json',
):
    print('file_path', file_path)
    body = _load_mock_data(file_path, mock_path) if mock_path else None
    responses.add(method, url, body=body, status=status_code, content_type=content_type)
