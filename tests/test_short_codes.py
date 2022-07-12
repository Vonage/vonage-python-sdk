from util import *


@responses.activate
def test_send_2fa_message(short_codes, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/sc/us/2fa/json")

    params = {"to": "16365553226", "pin": "1234"}

    assert isinstance(short_codes.send_2fa_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "to=16365553226" in request_body()
    assert "pin=1234" in request_body()


@responses.activate
def test_send_event_alert_message(short_codes, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/sc/us/alert/json")

    params = {"to": "16365553226", "server": "host", "link": "http://example.com/"}

    assert isinstance(short_codes.send_event_alert_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "to=16365553226" in request_body()
    assert "server=host" in request_body()
    assert "link=http%3A%2F%2Fexample.com%2F" in request_body()


@responses.activate
def test_send_marketing_message(short_codes, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/sc/us/marketing/json")

    params = {
        "from": "short-code",
        "to": "16365553226",
        "keyword": "NEXMO",
        "text": "Hello",
    }

    assert isinstance(short_codes.send_marketing_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "from=short-code" in request_body()
    assert "to=16365553226" in request_body()
    assert "keyword=NEXMO" in request_body()
    assert "text=Hello" in request_body()


@responses.activate
def test_get_event_alert_numbers(short_codes, dummy_data):
    stub(responses.GET, "https://rest.nexmo.com/sc/us/alert/opt-in/query/json")

    assert isinstance(short_codes.get_event_alert_numbers(), dict)
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_resubscribe_event_alert_number(short_codes, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/sc/us/alert/opt-in/manage/json")

    params = {"msisdn": "441632960960"}

    assert isinstance(short_codes.resubscribe_event_alert_number(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "msisdn=441632960960" in request_body()