from os.path import abspath

import responses
from pytest import raises
from vonage_http_client.http_client import HttpClient, HttpClientOptions
from vonage_identity_insights.errors import (
    EmptyInsightsRequestException,
    IdentityInsightsError,
)
from vonage_identity_insights.identity_insights import IdentityInsights
from vonage_identity_insights.requests import (
    EmptyInsight,
    IdentityInsightsRequest,
    InsightsRequest,
)

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)


options = HttpClientOptions(api_host="api-eu.vonage.com", timeout=30)
identity_insights = IdentityInsights(HttpClient(get_mock_jwt_auth(), options))


def test_http_client_property():
    http_client = identity_insights.http_client
    assert isinstance(http_client, HttpClient)


@responses.activate
def test_format_insight():
    build_response(
        path,
        'POST',
        'https://api-eu.vonage.com/identity-insights/v1/requests',
        'format.json',
    )

    options = IdentityInsightsRequest(
        phone_number="1234567890", insights=InsightsRequest(format=EmptyInsight())
    )

    response = identity_insights.requests(options)

    assert response.insights.format.status.code == "OK"
    assert response.insights.format.status.message == "Success"


@responses.activate
def test_basic_insight_error():
    build_response(
        path,
        'POST',
        'https://api-eu.vonage.com/identity-insights/v1/requests',
        'insight_error.json',
    )

    options = IdentityInsightsRequest(
        phone_number="1234567890", insights=InsightsRequest(format=EmptyInsight())
    )

    with raises(IdentityInsightsError) as e:
        identity_insights.requests(options)

    assert "Malformed JSON" in str(e.value)


@responses.activate
def test_empty_insights_request_raises_exception():
    options = IdentityInsightsRequest(
        phone_number="1234567890", insights=InsightsRequest()
    )

    with raises(EmptyInsightsRequestException):
        identity_insights.requests(options)


@responses.activate
def test_nullable_response_fields():
    build_response(
        path,
        'POST',
        'https://api-eu.vonage.com/identity-insights/v1/requests',
        'nullable_response.json',
    )

    options = IdentityInsightsRequest(
        phone_number="1234567890", insights=InsightsRequest(format=EmptyInsight())
    )

    response = identity_insights.requests(options)

    # Verify that optional fields with missing values are None
    assert response.insights.format.country_code is None
    assert response.insights.format.country_name is None
    assert response.insights.format.time_zones is None
    assert response.insights.format.is_format_valid is None
    assert response.insights.format.status.code == "OK"
    assert response.insights.format.status.message is None

    # Verify original_carrier fields are None when not provided
    assert response.insights.original_carrier.name is None
    assert response.insights.original_carrier.network_type is None
    assert response.insights.original_carrier.country_code is None
    assert response.insights.original_carrier.network_code is None
    assert response.insights.original_carrier.status.code == "OK"
    assert response.insights.original_carrier.status.message == "Success"
