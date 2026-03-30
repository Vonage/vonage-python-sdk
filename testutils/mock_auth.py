from base64 import b64encode
from os.path import dirname, join

from vonage_http_client.auth import Auth

test_api_key = 'test_api_key'
test_api_secret = 'test_api_secret'


def read_file(path):
    """Read a file from the testutils/data directory."""

    with open(join(dirname(__file__), path)) as input_file:
        return input_file.read()


def get_base64_encoded_api_key_and_secret():
    """Return a base64 encoded string of the API key and secret."""

    return b64encode(f'{test_api_key}:{test_api_secret}'.encode('utf-8')).decode('ascii')


def get_mock_api_key_auth():
    """Return an Auth object with an API key and secret."""

    return Auth(api_key=test_api_key, api_secret=test_api_secret)


def get_mock_jwt_auth():
    """Return an Auth object with a JWT."""

    return Auth(
        application_id='test_application_id',
        private_key=read_file('data/fake_private_key.txt'),
    )
