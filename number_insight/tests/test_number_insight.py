from os.path import abspath

import responses
from pytest import raises
from vonage_http_client.http_client import HttpClient
from vonage_number_insight.errors import NumberInsightError
from vonage_number_insight.number_insight import NumberInsight
from vonage_number_insight.requests import BasicInsightRequest

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
    response = number_insight.basic_number_insight(options)
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
        number_insight.basic_number_insight(options)
    assert e.match('Invalid request :: Not valid number format detected')
    assert 0
