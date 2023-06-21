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
        import vonage

        self.api_key = "nexmo-api-key"
        self.api_secret = "nexmo-api-secret"
        self.signature_secret = "secret"
        self.application_id = "nexmo-application-id"
        self.private_key = read_file("data/private_key.txt")
        self.public_key = read_file("data/public_key.txt")
        self.user_agent = f"vonage-python/{vonage.__version__} python/{platform.python_version()}"
        self.host = "rest.nexmo.com"
        self.api_host = "api.nexmo.com"
        self.meetings_api_host = "api-eu.vonage.com/beta/meetings"


@pytest.fixture(scope="session")
def dummy_data():
    return DummyData()


@pytest.fixture
def client(dummy_data):
    import vonage

    return vonage.Client(
        key=dummy_data.api_key,
        secret=dummy_data.api_secret,
        application_id=dummy_data.application_id,
        private_key=dummy_data.private_key,
    )


# Represents an instance of the Voice class for testing
@pytest.fixture
def voice(client):
    import vonage

    return vonage.Voice(client)


# Represents an instance of the Sms class for testing
@pytest.fixture
def sms(client):
    import vonage

    return vonage.Sms(client)


# Represents an instance of the Verify class for testing
@pytest.fixture
def verify(client):
    import vonage

    return vonage.Verify(client)


@pytest.fixture
def number_insight(client):
    import vonage

    return vonage.NumberInsight(client)


@pytest.fixture
def account(client):
    import vonage

    return vonage.Account(client)


@pytest.fixture
def numbers(client):
    import vonage

    return vonage.Numbers(client)


@pytest.fixture
def ussd(client):
    import vonage

    return vonage.Ussd(client)


@pytest.fixture
def short_codes(client):
    import vonage

    return vonage.ShortCodes(client)


@pytest.fixture
def messages(client):
    import vonage

    return vonage.Messages(client)


@pytest.fixture
def redact(client):
    import vonage

    return vonage.Redact(client)


@pytest.fixture
def application_v2(client):
    import vonage

    return vonage.ApplicationV2(client)


@pytest.fixture
def meetings(client):
    import vonage

    return vonage.Meetings(client)


@pytest.fixture
def proc(client):
    import vonage

    return vonage.ProactiveConnect(client)
