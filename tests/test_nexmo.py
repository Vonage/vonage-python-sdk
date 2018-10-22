import nexmo
from util import *

import sys

if sys.version_info[0] == 3:
    bytes_type = bytes
else:
    bytes_type = str


@responses.activate
def test_send_ussd_push_message(client, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/ussd/json")

    params = {"from": "MyCompany20", "to": "447525856424", "text": "Hello"}

    assert isinstance(client.send_ussd_push_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "from=MyCompany20" in request_body()
    assert "to=447525856424" in request_body()
    assert "text=Hello" in request_body()


@responses.activate
def test_send_ussd_prompt_message(client, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/ussd-prompt/json")

    params = {"from": "long-virtual-number", "to": "447525856424", "text": "Hello"}

    assert isinstance(client.send_ussd_prompt_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "from=long-virtual-number" in request_body()
    assert "to=447525856424" in request_body()
    assert "text=Hello" in request_body()


@responses.activate
def test_send_2fa_message(client, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/sc/us/2fa/json")

    params = {"to": "16365553226", "pin": "1234"}

    assert isinstance(client.send_2fa_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "to=16365553226" in request_body()
    assert "pin=1234" in request_body()


@responses.activate
def test_send_event_alert_message(client, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/sc/us/alert/json")

    params = {"to": "16365553226", "server": "host", "link": "http://example.com/"}

    assert isinstance(client.send_event_alert_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "to=16365553226" in request_body()
    assert "server=host" in request_body()
    assert "link=http%3A%2F%2Fexample.com%2F" in request_body()


@responses.activate
def test_send_marketing_message(client, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/sc/us/marketing/json")

    params = {
        "from": "short-code",
        "to": "16365553226",
        "keyword": "NEXMO",
        "text": "Hello",
    }

    assert isinstance(client.send_marketing_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "from=short-code" in request_body()
    assert "to=16365553226" in request_body()
    assert "keyword=NEXMO" in request_body()
    assert "text=Hello" in request_body()


@responses.activate
def test_get_event_alert_numbers(client, dummy_data):
    stub(responses.GET, "https://rest.nexmo.com/sc/us/alert/opt-in/query/json")

    assert isinstance(client.get_event_alert_numbers(), dict)
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_resubscribe_event_alert_number(client, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/sc/us/alert/opt-in/manage/json")

    params = {"msisdn": "441632960960"}

    assert isinstance(client.resubscribe_event_alert_number(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "msisdn=441632960960" in request_body()


def test_check_signature(dummy_data):
    params = {
        "a": "1",
        "b": "2",
        "timestamp": "1461605396",
        "sig": "6af838ef94998832dbfc29020b564830",
    }

    client = nexmo.Client(
        key=dummy_data.api_key, secret=dummy_data.api_secret, signature_secret="secret"
    )

    assert client.check_signature(params)


def test_signature(client, dummy_data):
    params = {"a": "1", "b": "2", "timestamp": "1461605396"}
    client = nexmo.Client(
        key=dummy_data.api_key, secret=dummy_data.api_secret, signature_secret="secret"
    )
    assert client.signature(params) == "6af838ef94998832dbfc29020b564830"


def test_signature_adds_timestamp(dummy_data):
    params = {"a=7": "1", "b": "2 & 5"}

    client = nexmo.Client(
        key=dummy_data.api_key, secret=dummy_data.api_secret, signature_secret="secret"
    )

    client.signature(params)
    assert params["timestamp"] is not None


def test_signature_md5(dummy_data):
    params = {"a": "1", "b": "2", "timestamp": "1461605396"}
    client = nexmo.Client(
        key=dummy_data.api_key,
        secret=dummy_data.api_secret,
        signature_secret=dummy_data.signature_secret,
        signature_method="md5",
    )
    assert client.signature(params) == "c15c21ced558c93a226c305f58f902f2"


def test_signature_sha1(dummy_data):
    params = {"a": "1", "b": "2", "timestamp": "1461605396"}
    client = nexmo.Client(
        key=dummy_data.api_key,
        secret=dummy_data.api_secret,
        signature_secret=dummy_data.signature_secret,
        signature_method="sha1",
    )
    assert client.signature(params) == "3e19a4e6880fdc2c1426bfd0587c98b9532f0210"


def test_signature_sha256(dummy_data):
    params = {"a": "1", "b": "2", "timestamp": "1461605396"}
    client = nexmo.Client(
        key=dummy_data.api_key,
        secret=dummy_data.api_secret,
        signature_secret=dummy_data.signature_secret,
        signature_method="sha256",
    )
    assert (
        client.signature(params)
        == "a321e824b9b816be7c3f28859a31749a098713d39f613c80d455bbaffae1cd24"
    )


def test_signature_sha512(dummy_data):
    params = {"a": "1", "b": "2", "timestamp": "1461605396"}
    client = nexmo.Client(
        key=dummy_data.api_key,
        secret=dummy_data.api_secret,
        signature_secret=dummy_data.signature_secret,
        signature_method="sha512",
    )
    assert (
        client.signature(params)
        == "812a18f76680fa0fe1b8bd9ee1625466ceb1bd96242e4d050d2cfd9a7b40166c63ed26ec9702168781b6edcf1633db8ff95af9341701004eec3fcf9550572ee8"
    )


def test_client_doesnt_require_api_key():
    client = nexmo.Client(application_id="myid", private_key="abc\nde")
    assert client is not None
    assert client.api_key is None
    assert client.api_secret is None


@responses.activate
def test_client_can_make_application_requests_without_api_key(dummy_data):
    stub(responses.POST, "https://api.nexmo.com/v1/calls")

    client = nexmo.Client(application_id="myid", private_key=dummy_data.private_key)
    client.create_call("123455")


@responses.activate
def test_get_recording(client, dummy_data):
    stub_bytes(
        responses.GET,
        "https://api.nexmo.com/v1/files/d6e47a2e-3414-11e8-8c2c-2f8b643ed957",
    )

    assert isinstance(
        client.get_recording(
            "https://api.nexmo.com/v1/files/d6e47a2e-3414-11e8-8c2c-2f8b643ed957"
        ),
        bytes_type,
    )
    assert request_user_agent() == dummy_data.user_agent
