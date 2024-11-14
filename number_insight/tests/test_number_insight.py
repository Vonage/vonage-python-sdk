from os.path import abspath

import responses
from pytest import raises
from vonage_http_client.http_client import HttpClient
from vonage_number_insight.errors import NumberInsightError
from vonage_number_insight.number_insight import NumberInsight
from vonage_number_insight.requests import (
    AdvancedAsyncInsightRequest,
    AdvancedSyncInsightRequest,
    BasicInsightRequest,
    StandardInsightRequest,
)

from testutils import build_response, get_mock_api_key_auth

path = abspath(__file__)


number_insight = NumberInsight(HttpClient(get_mock_api_key_auth()))


def test_http_client_property():
    http_client = number_insight.http_client
    assert isinstance(http_client, HttpClient)


@responses.activate
def test_basic_insight():
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/ni/basic/json',
        'basic_insight.json',
    )
    options = BasicInsightRequest(number='12345678900', country_code='US')
    response = number_insight.get_basic_info(options)
    assert response.status == 0
    assert response.status_message == 'Success'


@responses.activate
def test_basic_insight_error():
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/ni/basic/json',
        'basic_insight_error.json',
    )

    with raises(NumberInsightError) as e:
        options = BasicInsightRequest(number='1234567890', country_code='US')
        number_insight.get_basic_info(options)
    assert e.match('Invalid request :: Not valid number format detected')


@responses.activate
def test_standard_insight():
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/ni/standard/json',
        'standard_insight.json',
    )
    options = StandardInsightRequest(number='12345678900', country_code='US', cnam=True)
    response = number_insight.get_standard_info(options)
    assert response.status == 0
    assert response.status_message == 'Success'
    assert response.current_carrier.network_code == '23415'
    assert response.original_carrier.network_type == 'mobile'
    assert response.caller_identity.caller_name == 'John Smith'


@responses.activate
def test_advanced_async_insight():
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/ni/advanced/async/json',
        'advanced_async_insight.json',
    )
    options = AdvancedAsyncInsightRequest(
        callback='https://example.com/callback',
        number='447700900000',
        country_code='GB',
        cnam=True,
    )
    response = number_insight.get_advanced_info_async(options)
    assert response.status == 0
    assert response.request_id == '434205b5-90ec-4ee2-a337-7b40d9683420'
    assert response.number == '447700900000'
    assert response.remaining_balance == '32.92665294'


@responses.activate
def test_advanced_async_insight_error():
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/ni/advanced/async/json',
        'advanced_async_insight_error.json',
    )

    options = AdvancedAsyncInsightRequest(
        callback='https://example.com/callback',
        number='447700900000',
        country_code='GB',
        cnam=True,
    )
    with raises(NumberInsightError) as e:
        number_insight.get_advanced_info_async(options)
    assert e.match('Invalid credentials')


@responses.activate
def test_advanced_async_insight_partial_error(caplog):
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/ni/advanced/async/json',
        'advanced_async_insight_partial_error.json',
    )

    options = AdvancedAsyncInsightRequest(
        callback='https://example.com/callback',
        number='447700900000',
        country_code='GB',
        cnam=True,
    )
    response = number_insight.get_advanced_info_async(options)
    assert 'Not all parameters are available' in caplog.text
    assert response.status == 43


@responses.activate
def test_advanced_sync_insight(caplog):
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/ni/advanced/json',
        'advanced_sync_insight.json',
    )
    options = AdvancedSyncInsightRequest(
        number='12345678900', country_code='US', cnam=True
    )
    response = number_insight.get_advanced_info_sync(options)

    assert 'Not all parameters are available' in caplog.text
    assert response.status == 44
    assert response.request_id == '97e973e7-2e27-4fd3-9e1a-972ea14dd992'
    assert response.current_carrier.network_code == '310090'
    assert response.caller_identity.first_name == 'John'
    assert response.caller_identity.last_name == 'Smith'
    assert response.caller_identity.subscription_type == 'postpaid'
    assert response.lookup_outcome == 1
    assert response.lookup_outcome_message == 'Partial success - some fields populated'
    assert response.roaming == 'unknown'
    assert response.status_message == 'Lookup Handler unable to handle request'
    assert response.valid_number == 'valid'
