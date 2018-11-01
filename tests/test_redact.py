from util import *


@responses.activate
def test_redact_transaction(client, dummy_data):
    responses.add(
        responses.POST,
        "https://api.nexmo.com/v1/redact/transaction",
        body=None,
        status=204,
    )

    assert client.redact_transaction(id="not-a-real-id", product="sms") is None
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"

@responses.activate
def test_redact_transaction_with_type(client, dummy_data):
    responses.add(
        responses.POST,
        "https://api.nexmo.com/v1/redact/transaction",
        body=None,
        status=204,
    )

    assert client.redact_transaction(id="some-id", product="sms", type="xyz") is None
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"
    assert b"xyz" in request_body()
