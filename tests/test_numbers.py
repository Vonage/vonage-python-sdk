from util import *


@responses.activate
def test_get_available_numbers(client, dummy_data):
    stub(responses.GET, "https://rest.nexmo.com/number/search")

    assert isinstance(client.get_available_numbers("CA", size=25), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "country=CA" in request_query()
    assert "size=25" in request_query()


@responses.activate
def test_buy_number(client, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/number/buy")

    params = {"country": "US", "msisdn": "number"}

    assert isinstance(client.buy_number(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "country=US" in request_body()
    assert "msisdn=number" in request_body()


@responses.activate
def test_cancel_number(client, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/number/cancel")

    params = {"country": "US", "msisdn": "number"}

    assert isinstance(client.cancel_number(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "country=US" in request_body()
    assert "msisdn=number" in request_body()


@responses.activate
def test_update_number(client, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/number/update")

    params = {"country": "US", "msisdn": "number", "moHttpUrl": "callback"}

    assert isinstance(client.update_number(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "country=US" in request_body()
    assert "msisdn=number" in request_body()
    assert "moHttpUrl=callback" in request_body()
