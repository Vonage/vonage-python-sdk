from os.path import abspath

import responses
from pytest import raises
from vonage_http_client.errors import HttpRequestError
from vonage_http_client.http_client import HttpClient
from vonage_network_auth import NetworkAuth
from vonage_network_auth.responses import OidcResponse

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)


network_auth = NetworkAuth(HttpClient(get_mock_jwt_auth()))


def test_http_client_property():
    http_client = network_auth.http_client
    assert isinstance(http_client, HttpClient)


@responses.activate
def test_oidc_request():
    build_response(
        path,
        'POST',
        'https://api-eu.vonage.com/oauth2/bc-authorize',
        'oidc_request.json',
    )

    response = network_auth.make_oidc_auth_id_request(
        number='447700900000',
        scope='dpv:FraudPreventionAndDetection#check-sim-swap',
    )

    assert response.auth_req_id == 'arid/8b0d35f3-4627-487c-a776-aegtdsf4rsd2'
    assert response.expires_in == 300
    assert response.interval == 0


@responses.activate
def test_sim_swap_token():
    build_response(
        path,
        'POST',
        'https://api-eu.vonage.com/oauth2/token',
        'token_request.json',
    )

    oidc_response_dict = {
        'auth_req_id': '0dadaeb4-7c79-4d39-b4b0-5a6cc08bf537',
        'expires_in': '120',
        'interval': '2',
    }
    oidc_response = OidcResponse(**oidc_response_dict)
    response = network_auth.request_sim_swap_access_token(oidc_response.auth_req_id)

    assert (
        response.access_token
        == 'eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vYW51YmlzLWNlcnRzLWMxLWV1dzEucHJvZC52MS52b25hZ2VuZXR3b3Jrcy5uZXQvandrcyIsImtpZCI6IkNOPVZvbmFnZSAxdmFwaWd3IEludGVybmFsIENBOjoxOTUxODQ2ODA3NDg1NTYwNjYzODY3MTM0NjE2MjU2MTU5MjU2NDkiLCJ0eXAiOiJKV1QiLCJ4NXUiOiJodHRwczovL2FudWJpcy1jZXJ0cy1jMS1ldXcxLnByb2QudjEudm9uYWdlbmV0d29ya3MubmV0L3YxL2NlcnRzLzA4NjliNDMyZTEzZmIyMzcwZTk2ZGI4YmUxMDc4MjJkIn0.eyJwcmluY2lwYWwiOnsiYXBpS2V5IjoiNGI1MmMwMGUiLCJhcHBsaWNhdGlvbklkIjoiMmJlZTViZWQtNmZlZS00ZjM2LTkxNmQtNWUzYjRjZDI1MjQzIiwibWFzdGVyQWNjb3VudElkIjoiNGI1MmMwMGUiLCJjYXBhYmlsaXRpZXMiOlsibmV0d29yay1hcGktZmVhdHVyZXMiXSwiZXh0cmFDb25maWciOnsiY2FtYXJhU3RhdGUiOiJmb0ZyQndnOFNmeGMydnd2S1o5Y3UrMlgrT0s1K2FvOWhJTTVGUGZMQ1dOeUlMTHR3WmY1dFRKbDdUc1p4QnY4QWx3aHM2bFNWcGVvVkhoWngvM3hUenFRWVkwcHpIZE5XL085ZEdRN1RKOE9sU1lDdTFYYXFEcnNFbEF4WEJVcUpGdnZTTkp5a1A5ZDBYWVN4ajZFd0F6UUFsNGluQjE1c3VMRFNsKy82U1FDa29Udnpld0tvcFRZb0F5MVg2dDJVWXdEVWFDNjZuOS9kVWxIemN3V0NGK3QwOGNReGxZVUxKZyt3T0hwV2xvWGx1MGc3REx0SCtHd0pvRGJoYnMyT2hVY3BobGZqajBpeHQ1OTRsSG5sQ1NYNkZrMmhvWEhKUW01S3JtOVBKSmttK0xTRjVsRTd3NUxtWTRvYTFXSGpkY0dwV1VsQlNQY000YnprOGU0bVE9PSJ9fSwiZmVkZXJhdGVkQXNzZXJ0aW9ucyI6e30sImF1ZCI6ImFwaS1ldS52b25hZ2UuY29tIiwiZXhwIjoxNzE3MDkyODY4LCJqdGkiOiJmNDZhYTViOC1hODA2LTRjMzctODQyMS02OGYwMzJjNDlhMWYiLCJpYXQiOjE3MTcwOTE5NzAsImlzcyI6IlZJQU0tSUFQIiwibmJmIjoxNzE3MDkxOTU1fQ.iLUbyDPR1HGLKh29fy6fqK65Q1O7mjWOletAEPJD4eu7gb0E85EL4M9R7ckJq5lIvgedQt3vBheTaON9_u-VYjMqo8ulPoEoGUDHbOzNbs4MmCW0_CRdDPGyxnUhvcbuJhPgnEHxmfHjJBljncUnk-Z7XCgyNajBNXeQQnHkRF_6NMngxJ-qjjhqbYL0VsF_JS7-TXxixNL0KAFl0SeN2DjkfwRBCclP-69CTExDjyOvouAcchqi-6ZYj_tXPCrTADuzUrQrW8C5nHp2-XjWJSFKzyvi48n8V1U6KseV-eYzBzvy7bJf0tRMX7G6gctTYq3DxdC_eXvXlnp1zx16mg'
    )
    assert response.token_type == 'bearer'
    assert response.expires_in == 29


@responses.activate
def test_whole_oauth2_flow():
    build_response(
        path,
        'POST',
        'https://api-eu.vonage.com/oauth2/bc-authorize',
        'oidc_request.json',
    )
    build_response(
        path,
        'POST',
        'https://api-eu.vonage.com/oauth2/token',
        'token_request.json',
    )

    access_token = network_auth.get_sim_swap_camara_token(
        number='447700900000', scope='dpv:FraudPreventionAndDetection#check-sim-swap'
    )
    assert (
        access_token
        == 'eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vYW51YmlzLWNlcnRzLWMxLWV1dzEucHJvZC52MS52b25hZ2VuZXR3b3Jrcy5uZXQvandrcyIsImtpZCI6IkNOPVZvbmFnZSAxdmFwaWd3IEludGVybmFsIENBOjoxOTUxODQ2ODA3NDg1NTYwNjYzODY3MTM0NjE2MjU2MTU5MjU2NDkiLCJ0eXAiOiJKV1QiLCJ4NXUiOiJodHRwczovL2FudWJpcy1jZXJ0cy1jMS1ldXcxLnByb2QudjEudm9uYWdlbmV0d29ya3MubmV0L3YxL2NlcnRzLzA4NjliNDMyZTEzZmIyMzcwZTk2ZGI4YmUxMDc4MjJkIn0.eyJwcmluY2lwYWwiOnsiYXBpS2V5IjoiNGI1MmMwMGUiLCJhcHBsaWNhdGlvbklkIjoiMmJlZTViZWQtNmZlZS00ZjM2LTkxNmQtNWUzYjRjZDI1MjQzIiwibWFzdGVyQWNjb3VudElkIjoiNGI1MmMwMGUiLCJjYXBhYmlsaXRpZXMiOlsibmV0d29yay1hcGktZmVhdHVyZXMiXSwiZXh0cmFDb25maWciOnsiY2FtYXJhU3RhdGUiOiJmb0ZyQndnOFNmeGMydnd2S1o5Y3UrMlgrT0s1K2FvOWhJTTVGUGZMQ1dOeUlMTHR3WmY1dFRKbDdUc1p4QnY4QWx3aHM2bFNWcGVvVkhoWngvM3hUenFRWVkwcHpIZE5XL085ZEdRN1RKOE9sU1lDdTFYYXFEcnNFbEF4WEJVcUpGdnZTTkp5a1A5ZDBYWVN4ajZFd0F6UUFsNGluQjE1c3VMRFNsKy82U1FDa29Udnpld0tvcFRZb0F5MVg2dDJVWXdEVWFDNjZuOS9kVWxIemN3V0NGK3QwOGNReGxZVUxKZyt3T0hwV2xvWGx1MGc3REx0SCtHd0pvRGJoYnMyT2hVY3BobGZqajBpeHQ1OTRsSG5sQ1NYNkZrMmhvWEhKUW01S3JtOVBKSmttK0xTRjVsRTd3NUxtWTRvYTFXSGpkY0dwV1VsQlNQY000YnprOGU0bVE9PSJ9fSwiZmVkZXJhdGVkQXNzZXJ0aW9ucyI6e30sImF1ZCI6ImFwaS1ldS52b25hZ2UuY29tIiwiZXhwIjoxNzE3MDkyODY4LCJqdGkiOiJmNDZhYTViOC1hODA2LTRjMzctODQyMS02OGYwMzJjNDlhMWYiLCJpYXQiOjE3MTcwOTE5NzAsImlzcyI6IlZJQU0tSUFQIiwibmJmIjoxNzE3MDkxOTU1fQ.iLUbyDPR1HGLKh29fy6fqK65Q1O7mjWOletAEPJD4eu7gb0E85EL4M9R7ckJq5lIvgedQt3vBheTaON9_u-VYjMqo8ulPoEoGUDHbOzNbs4MmCW0_CRdDPGyxnUhvcbuJhPgnEHxmfHjJBljncUnk-Z7XCgyNajBNXeQQnHkRF_6NMngxJ-qjjhqbYL0VsF_JS7-TXxixNL0KAFl0SeN2DjkfwRBCclP-69CTExDjyOvouAcchqi-6ZYj_tXPCrTADuzUrQrW8C5nHp2-XjWJSFKzyvi48n8V1U6KseV-eYzBzvy7bJf0tRMX7G6gctTYq3DxdC_eXvXlnp1zx16mg'
    )


def test_number_plus_prefixes():
    assert network_auth._ensure_plus_prefix('447700900000') == '+447700900000'
    assert network_auth._ensure_plus_prefix('+447700900000') == '+447700900000'


@responses.activate
def test_oidc_request_permissions_error():
    build_response(
        path,
        'POST',
        'https://api-eu.vonage.com/oauth2/bc-authorize',
        'oidc_request_permissions_error.json',
        status_code=400,
    )

    with raises(HttpRequestError) as err:
        network_auth.make_oidc_auth_id_request(
            number='447700900000',
            scope='dpv:FraudPreventionAndDetection#check-sim-swap',
        )
    assert err.match('"title": "Bad Request"')


def test_get_oidc_url():
    url_options = {
        'redirect_uri': 'https://example.com/callback',
        'state': 'state_id',
        'login_hint': '447700900000',
    }
    response = network_auth.get_oidc_url(url_options)

    assert (
        response
        == 'https://oidc.idp.vonage.com/oauth2/auth?client_id=test_application_id&redirect_uri=https%3A%2F%2Fexample.com%2Fcallback&response_type=code&scope=openid+dpv%3AFraudPreventionAndDetection%23number-verification-verify-read&state=state_id&login_hint=%2B447700900000'
    )


@responses.activate
def test_get_number_verification_camara_token():
    build_response(
        path,
        'POST',
        'https://api-eu.vonage.com/oauth2/token',
        'token_request.json',
    )
    token = network_auth.get_number_verification_camara_token(
        'code', 'https://example.com/redirect'
    )

    assert (
        token
        == 'eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vYW51YmlzLWNlcnRzLWMxLWV1dzEucHJvZC52MS52b25hZ2VuZXR3b3Jrcy5uZXQvandrcyIsImtpZCI6IkNOPVZvbmFnZSAxdmFwaWd3IEludGVybmFsIENBOjoxOTUxODQ2ODA3NDg1NTYwNjYzODY3MTM0NjE2MjU2MTU5MjU2NDkiLCJ0eXAiOiJKV1QiLCJ4NXUiOiJodHRwczovL2FudWJpcy1jZXJ0cy1jMS1ldXcxLnByb2QudjEudm9uYWdlbmV0d29ya3MubmV0L3YxL2NlcnRzLzA4NjliNDMyZTEzZmIyMzcwZTk2ZGI4YmUxMDc4MjJkIn0.eyJwcmluY2lwYWwiOnsiYXBpS2V5IjoiNGI1MmMwMGUiLCJhcHBsaWNhdGlvbklkIjoiMmJlZTViZWQtNmZlZS00ZjM2LTkxNmQtNWUzYjRjZDI1MjQzIiwibWFzdGVyQWNjb3VudElkIjoiNGI1MmMwMGUiLCJjYXBhYmlsaXRpZXMiOlsibmV0d29yay1hcGktZmVhdHVyZXMiXSwiZXh0cmFDb25maWciOnsiY2FtYXJhU3RhdGUiOiJmb0ZyQndnOFNmeGMydnd2S1o5Y3UrMlgrT0s1K2FvOWhJTTVGUGZMQ1dOeUlMTHR3WmY1dFRKbDdUc1p4QnY4QWx3aHM2bFNWcGVvVkhoWngvM3hUenFRWVkwcHpIZE5XL085ZEdRN1RKOE9sU1lDdTFYYXFEcnNFbEF4WEJVcUpGdnZTTkp5a1A5ZDBYWVN4ajZFd0F6UUFsNGluQjE1c3VMRFNsKy82U1FDa29Udnpld0tvcFRZb0F5MVg2dDJVWXdEVWFDNjZuOS9kVWxIemN3V0NGK3QwOGNReGxZVUxKZyt3T0hwV2xvWGx1MGc3REx0SCtHd0pvRGJoYnMyT2hVY3BobGZqajBpeHQ1OTRsSG5sQ1NYNkZrMmhvWEhKUW01S3JtOVBKSmttK0xTRjVsRTd3NUxtWTRvYTFXSGpkY0dwV1VsQlNQY000YnprOGU0bVE9PSJ9fSwiZmVkZXJhdGVkQXNzZXJ0aW9ucyI6e30sImF1ZCI6ImFwaS1ldS52b25hZ2UuY29tIiwiZXhwIjoxNzE3MDkyODY4LCJqdGkiOiJmNDZhYTViOC1hODA2LTRjMzctODQyMS02OGYwMzJjNDlhMWYiLCJpYXQiOjE3MTcwOTE5NzAsImlzcyI6IlZJQU0tSUFQIiwibmJmIjoxNzE3MDkxOTU1fQ.iLUbyDPR1HGLKh29fy6fqK65Q1O7mjWOletAEPJD4eu7gb0E85EL4M9R7ckJq5lIvgedQt3vBheTaON9_u-VYjMqo8ulPoEoGUDHbOzNbs4MmCW0_CRdDPGyxnUhvcbuJhPgnEHxmfHjJBljncUnk-Z7XCgyNajBNXeQQnHkRF_6NMngxJ-qjjhqbYL0VsF_JS7-TXxixNL0KAFl0SeN2DjkfwRBCclP-69CTExDjyOvouAcchqi-6ZYj_tXPCrTADuzUrQrW8C5nHp2-XjWJSFKzyvi48n8V1U6KseV-eYzBzvy7bJf0tRMX7G6gctTYq3DxdC_eXvXlnp1zx16mg'
    )
