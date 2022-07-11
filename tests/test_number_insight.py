from util import *
from vonage.errors import CallbackRequiredError


@responses.activate
def test_get_basic_number_insight(number_insight, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/ni/basic/json")

    assert isinstance(number_insight.get_basic_number_insight(number="447525856424"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "number=447525856424" in request_query()


@responses.activate
def test_get_standard_number_insight(number_insight, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/ni/standard/json")

    assert isinstance(number_insight.get_standard_number_insight(number="447525856424"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "number=447525856424" in request_query()


@responses.activate
def test_get_advanced_number_insight(number_insight, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/ni/advanced/json")

    assert isinstance(number_insight.get_advanced_number_insight(number="447525856424"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "number=447525856424" in request_query()


@responses.activate
def test_get_async_advanced_number_insight(number_insight, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/ni/advanced/async/json")

    params = {"number": "447525856424", "callback": "https://example.com"}

    assert isinstance(number_insight.get_async_advanced_number_insight(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "number=447525856424" in request_query()
    assert "callback=https%3A%2F%2Fexample.com" in request_query()

def test_callback_required_error_async_advanced_number_insight(number_insight, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/ni/advanced/async/json")

    params = {"number": "447525856424", "callback": ""}

    with pytest.raises(CallbackRequiredError):
        number_insight.get_async_advanced_number_insight(params)
