from util import *

@responses.activate
def test_send_ussd_push_message(ussd, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/ussd/json")

    params = {"from": "MyCompany20", "to": "447525856424", "text": "Hello"}

    assert isinstance(ussd.send_ussd_push_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "from=MyCompany20" in request_body()
    assert "to=447525856424" in request_body()
    assert "text=Hello" in request_body()

@responses.activate
def test_send_ussd_prompt_message(ussd, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/ussd-prompt/json")

    params = {"from": "long-virtual-number", "to": "447525856424", "text": "Hello"}

    assert isinstance(ussd.send_ussd_prompt_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "from=long-virtual-number" in request_body()
    assert "to=447525856424" in request_body()
    assert "text=Hello" in request_body()