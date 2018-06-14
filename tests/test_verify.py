from util import *


@responses.activate
def test_start_verification(client, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/verify/json")

    params = {"number": "447525856424", "brand": "MyApp"}

    assert isinstance(client.start_verification(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "number=447525856424" in request_body()
    assert "brand=MyApp" in request_body()


@responses.activate
def test_send_verification_request(client, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/verify/json")

    params = {"number": "447525856424", "brand": "MyApp"}

    assert isinstance(client.send_verification_request(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "number=447525856424" in request_body()
    assert "brand=MyApp" in request_body()


@responses.activate
def test_check_verification(client, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/verify/check/json")

    assert isinstance(
        client.check_verification("8g88g88eg8g8gg9g90", code="123445"), dict
    )
    assert request_user_agent() == dummy_data.user_agent
    assert "code=123445" in request_body()
    assert "request_id=8g88g88eg8g8gg9g90" in request_body()


@responses.activate
def test_check_verification_request(client, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/verify/check/json")

    params = {"code": "123445", "request_id": "8g88g88eg8g8gg9g90"}

    assert isinstance(client.check_verification_request(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "code=123445" in request_body()
    assert "request_id=8g88g88eg8g8gg9g90" in request_body()


@responses.activate
def test_get_verification(client, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/verify/search/json")

    assert isinstance(client.get_verification("xxx"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "request_id=xxx" in request_query()


@responses.activate
def test_get_verification_request(client, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/verify/search/json")

    assert isinstance(client.get_verification_request("xxx"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "request_id=xxx" in request_query()


@responses.activate
def test_cancel_verification(client, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/verify/control/json")

    assert isinstance(client.cancel_verification("8g88g88eg8g8gg9g90"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "cmd=cancel" in request_body()
    assert "request_id=8g88g88eg8g8gg9g90" in request_body()


@responses.activate
def test_trigger_next_verification_event(client, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/verify/control/json")

    assert isinstance(
        client.trigger_next_verification_event("8g88g88eg8g8gg9g90"), dict
    )
    assert request_user_agent() == dummy_data.user_agent
    assert "cmd=trigger_next_event" in request_body()
    assert "request_id=8g88g88eg8g8gg9g90" in request_body()


@responses.activate
def test_control_verification_request(client, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/verify/control/json")

    params = {"cmd": "cancel", "request_id": "8g88g88eg8g8gg9g90"}

    assert isinstance(client.control_verification_request(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "cmd=cancel" in request_body()
    assert "request_id=8g88g88eg8g8gg9g90" in request_body()
