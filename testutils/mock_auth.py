from os.path import join, dirname

from vonage_http_client.auth import Auth


def read_file(path):
    with open(join(dirname(__file__), path)) as input_file:
        return input_file.read()


def get_mock_api_key_auth():
    return Auth(api_key='test_api_key', api_secret='test_api_secret')


def get_mock_jwt_auth():
    return Auth(
        application_id='test_application_id',
        private_key=read_file('data/fake_private_key.txt'),
    )
