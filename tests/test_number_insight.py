from util import *
from vonage.errors import CallbackRequiredError, NumberInsightError


@responses.activate
def test_get_basic_number_insight(number_insight, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/ni/basic/json",
        fixture_path='number_insight/basic_get.json')

    response = number_insight.get_basic_number_insight(number='447700900000')
    assert isinstance(response, dict)
    assert response['status_message'] == 'Success'
    assert request_user_agent() == dummy_data.user_agent
    assert "number=447700900000" in request_query()


@responses.activate
def test_get_basic_number_insight_error(number_insight):
    stub(responses.GET, "https://api.nexmo.com/ni/basic/json",
        fixture_path='number_insight/get_error.json')

    with pytest.raises(NumberInsightError) as err:
        number_insight.get_basic_number_insight(number='1234')
        assert str(err.value) == 'Number Insight API method failed with status: 3 and error: Invalid request :: Not valid number format detected [ 1234 ]'


@responses.activate
def test_get_standard_number_insight(number_insight, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/ni/standard/json",
        fixture_path='number_insight/standard_get.json')

    response = number_insight.get_standard_number_insight(number="447700900000")
    assert isinstance(response, dict)
    assert response['status_message'] == 'Success'
    assert request_user_agent() == dummy_data.user_agent
    assert "number=447700900000" in request_query()


@responses.activate
def test_get_standard_number_insight_error(number_insight):
    stub(responses.GET, "https://api.nexmo.com/ni/standard/json",
        fixture_path='number_insight/get_error.json')

    with pytest.raises(NumberInsightError) as err:
        number_insight.get_standard_number_insight(number='1234')
        assert str(err.value) == 'Number Insight API method failed with status: 3 and error: Invalid request :: Not valid number format detected [ 1234 ]'


@responses.activate
def test_get_advanced_number_insight(number_insight, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/ni/advanced/json",
        fixture_path='number_insight/advanced_get.json')

    response = number_insight.get_advanced_number_insight(number="447700900000")
    assert isinstance(response, dict)
    assert response['status_message'] == 'Success'
    assert request_user_agent() == dummy_data.user_agent
    assert "number=447700900000" in request_query()


@responses.activate
def test_get_advanced_number_insight_error(number_insight):
    stub(responses.GET, "https://api.nexmo.com/ni/advanced/json",
        fixture_path='number_insight/get_error.json')

    with pytest.raises(NumberInsightError) as err:
        number_insight.get_advanced_number_insight(number='1234')
        assert str(err.value) == 'Number Insight API method failed with status: 3 and error: Invalid request :: Not valid number format detected [ 1234 ]'

@responses.activate
def test_get_async_advanced_number_insight(number_insight, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/ni/advanced/async/json",
        fixture_path='number_insight/advanced_get.json')

    params = {"number": "447525856424", "callback": "https://example.com"}

    response = number_insight.get_async_advanced_number_insight(params)
    assert isinstance(response, dict)
    assert response['status_message'] == 'Success'
    assert request_user_agent() == dummy_data.user_agent
    assert "number=447525856424" in request_query()
    assert "callback=https%3A%2F%2Fexample.com" in request_query()


@responses.activate
def test_get_async_advanced_number_insight_error(number_insight):
    stub(responses.GET, "https://api.nexmo.com/ni/advanced/async/json",
        fixture_path='number_insight/get_async_error.json')

    with pytest.raises(NumberInsightError) as err:
        number_insight.get_async_advanced_number_insight(number='1234', callback='https://example.com')
        assert str(err.value) == 'Number Insight API method failed with status: 3 and error: Invalid request :: Not valid number format detected [ 1234 ]'


def test_callback_required_error_async_advanced_number_insight(number_insight, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/ni/advanced/async/json")

    params = {"number": "447525856424", "callback": ""}

    with pytest.raises(CallbackRequiredError):
        number_insight.get_async_advanced_number_insight(params)
