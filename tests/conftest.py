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
        from vonage import __version__

        self.api_key = "nexmo-api-key"
        self.api_secret = "nexmo-api-secret"
        self.signature_secret = "secret"
        self.application_id = "nexmo-application-id"
        self.private_key = read_file("data/private_key.txt")
        self.public_key = read_file("data/public_key.txt")
        self.user_agent = f"vonage-python/{__version__} python/{platform.python_version()}"
        self.host = "rest.nexmo.com"
        self.api_host = "api.nexmo.com"
        self.meetings_api_host = "api-eu.vonage.com/beta/meetings"


@pytest.fixture(scope="session")
def dummy_data():
    return DummyData()


@pytest.fixture
def client(dummy_data):
    from vonage.client import Client

    return Client(
        key=dummy_data.api_key,
        secret=dummy_data.api_secret,
        application_id=dummy_data.application_id,
        private_key=dummy_data.private_key,
    )


# Represents an instance of the Voice class for testing
@pytest.fixture
def voice(client):
    from vonage.voice import Voice

    return Voice(client)


# Represents an instance of the Sms class for testing
@pytest.fixture
def sms(client):
    from vonage.sms import Sms

    return Sms(client)


# Represents an instance of the Verify class for testing
@pytest.fixture
def verify(client):
    from vonage.verify import Verify

    return Verify(client)


@pytest.fixture
def number_insight(client):
    from vonage.number_insight import NumberInsight

    return NumberInsight(client)


@pytest.fixture
def account(client):
    from vonage.account import Account

    return Account(client)


@pytest.fixture
def numbers(client):
    from vonage.number_management import Numbers

    return Numbers(client)


@pytest.fixture
def ussd(client):
    from vonage.ussd import Ussd

    return Ussd(client)


@pytest.fixture
def short_codes(client):
    from vonage.short_codes import ShortCodes

    return ShortCodes(client)


@pytest.fixture
def messages(client):
    from vonage.messages import Messages

    return Messages(client)


@pytest.fixture
def redact(client):
    from vonage.redact import Redact

    return Redact(client)


@pytest.fixture
def application_v2(client):
    from vonage.application import Application

    return Application(client)


@pytest.fixture
def meetings(client):
    from vonage.meetings import Meetings

    return Meetings(client)


@pytest.fixture
def proc(client):
    from vonage.proactive_connect import ProactiveConnect

    return ProactiveConnect(client)


@pytest.fixture
def camara_auth(client):
    from vonage.camara_auth import CamaraAuth

    return CamaraAuth(client)


@pytest.fixture
def sim_swap(client):
    from vonage.sim_swap import SimSwap

    return SimSwap(client)


@pytest.fixture
def number_verification(client):
    from vonage.number_verification import NumberVerification

    return NumberVerification(client)
