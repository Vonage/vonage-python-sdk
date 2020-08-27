import os
import os.path
import platform

import pytest


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
        self.host = "rest.nexmo.com"
        self.api_host = "api.nexmo.com"


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

#Represents an instance of the Voice class for testing
@pytest.fixture
def voice(client, dummy_data):
    import nexmo

    return nexmo.Voice(
        client
    )

#Represents an instance of the Sms class for testing
@pytest.fixture
def sms(client, dummy_data):
    import nexmo

    return nexmo.Sms(
        client
    )

#Represents an instance of the Verify class for testing
@pytest.fixture
def verify(client, dummy_data):
    import nexmo

    return nexmo.Verify(
        client
    )
