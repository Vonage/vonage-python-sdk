from util import *


@responses.activate
def test_get_basic_number_insight(client, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/ni/basic/json")

    assert isinstance(client.get_basic_number_insight(number="447525856424"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "number=447525856424" in request_query()


@responses.activate
def test_get_standard_number_insight(client, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/ni/standard/json")

    assert isinstance(client.get_standard_number_insight(number="447525856424"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "number=447525856424" in request_query()


@responses.activate
def test_get_number_insight(client, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/number/lookup/json")

    assert isinstance(client.get_number_insight(number="447525856424"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "number=447525856424" in request_query()


@responses.activate
def test_get_advanced_number_insight(client, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/ni/advanced/json")

    assert isinstance(client.get_advanced_number_insight(number="447525856424"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "number=447525856424" in request_query()


@responses.activate
def test_request_number_insight(client, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/ni/json")

    params = {"number": "447525856424", "callback": "https://example.com"}

    assert isinstance(client.request_number_insight(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "number=447525856424" in request_body()
    assert "callback=https%3A%2F%2Fexample.com" in request_body()
