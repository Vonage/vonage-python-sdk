import os
import os.path
import platform

import jwt
import pytest

from util import request_params, request_headers


# Ensure our client isn't being configured with real values!
os.environ.clear()


def read_file(path):
    with open(os.path.join(os.path.dirname(__file__), path)) as input_file:
        return input_file.read()


class DummyData(object):
    def __init__(self):
        import nexmo

        self.api_key = "nexmo-api-key"
        self.api_secret = "nexmo-api-secret"
        self.signature_secret = "secret"
        self.application_id = "nexmo-application-id"
        self.private_key = read_file("data/private_key.txt")
        self.public_key = read_file("data/public_key.txt")
        self.user_agent = "nexmo-python/{} python/{}".format(
            nexmo.__version__, platform.python_version()
        )


@pytest.fixture(scope="session")
def dummy_data():
    return DummyData()


@pytest.fixture
def client(dummy_data):
    import nexmo

    return nexmo.Client(
        key=dummy_data.api_key,
        secret=dummy_data.api_secret,
        application_id=dummy_data.application_id,
        private_key=dummy_data.private_key,
    )


class AuthAssertions(object):
    def __init__(self, dummy_data):
        self._dummy_data = dummy_data

    def assert_jwt_auth(self):
        params = request_params()
        assert "api_key" not in params
        assert "api_secret" not in params
        encoded = request_headers()["Authorization"].split(b" ")[1]
        try:
            jwt.decode(encoded, self._dummy_data.public_key, algorithm="RS256")
        except jwt.DecodeError as de:
            raise pytest.fail("Invalid JWT authentication header: {}".format(de))


@pytest.fixture
def auth(dummy_data):
    return AuthAssertions(dummy_data)
