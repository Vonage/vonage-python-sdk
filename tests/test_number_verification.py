from vonage.errors import NumberVerificationError
from vonage.number_verification import NumberVerification
from util import *

import responses
from pytest import raises


def test_get_oidc_url(number_verification: NumberVerification):
    url = number_verification.get_oidc_url(
        redirect_uri='https://example.com/callback',
        state='state_id',
        login_hint='447700900000',
    )

    assert (
        url
        == 'https://oidc.idp.vonage.com/oauth2/auth?client_id=nexmo-application-id&redirect_uri=https%3A%2F%2Fexample.com%2Fcallback&response_type=code&scope=openid+dpv%3AFraudPreventionAndDetection%23number-verification-verify-read&state=state_id&login_hint=%2B447700900000'
    )


@responses.activate
def test_create_camara_token_and_verify_numbers(number_verification: NumberVerification):
    stub(
        responses.POST,
        'https://api-eu.vonage.com/oauth2/token',
        fixture_path='camara_auth/token_request.json',
    )

    access_token = number_verification.exchange_code_for_token(
        'code', 'https://example.com/callback'
    )
    assert (
        access_token
        == 'eyJhbGciOiJSUzI1NiIsImprdSI6Imh0dHBzOi8vYW51YmlzLWNlcnRzLWMxLWV1dzEucHJvZC52MS52b25hZ2VuZXR3b3Jrcy5uZXQvandrcyIsImtpZCI6IkNOPVZvbmFnZSAxdmFwaWd3IEludGVybmFsIENBOjoxOTUxODQ2ODA3NDg1NTYwNjYzODY3MTM0NjE2MjU2MTU5MjU2NDkiLCJ0eXAiOiJKV1QiLCJ4NXUiOiJodHRwczovL2FudWJpcy1jZXJ0cy1jMS1ldXcxLnByb2QudjEudm9uYWdlbmV0d29ya3MubmV0L3YxL2NlcnRzLzA4NjliNDMyZTEzZmIyMzcwZTk2ZGI4YmUxMDc4MjJkIn0.eyJwcmluY2lwYWwiOnsiYXBpS2V5IjoiNGI1MmMwMGUiLCJhcHBsaWNhdGlvbklkIjoiMmJlZTViZWQtNmZlZS00ZjM2LTkxNmQtNWUzYjRjZDI1MjQzIiwibWFzdGVyQWNjb3VudElkIjoiNGI1MmMwMGUiLCJjYXBhYmlsaXRpZXMiOlsibmV0d29yay1hcGktZmVhdHVyZXMiXSwiZXh0cmFDb25maWciOnsiY2FtYXJhU3RhdGUiOiJmb0ZyQndnOFNmeGMydnd2S1o5Y3UrMlgrT0s1K2FvOWhJTTVGUGZMQ1dOeUlMTHR3WmY1dFRKbDdUc1p4QnY4QWx3aHM2bFNWcGVvVkhoWngvM3hUenFRWVkwcHpIZE5XL085ZEdRN1RKOE9sU1lDdTFYYXFEcnNFbEF4WEJVcUpGdnZTTkp5a1A5ZDBYWVN4ajZFd0F6UUFsNGluQjE1c3VMRFNsKy82U1FDa29Udnpld0tvcFRZb0F5MVg2dDJVWXdEVWFDNjZuOS9kVWxIemN3V0NGK3QwOGNReGxZVUxKZyt3T0hwV2xvWGx1MGc3REx0SCtHd0pvRGJoYnMyT2hVY3BobGZqajBpeHQ1OTRsSG5sQ1NYNkZrMmhvWEhKUW01S3JtOVBKSmttK0xTRjVsRTd3NUxtWTRvYTFXSGpkY0dwV1VsQlNQY000YnprOGU0bVE9PSJ9fSwiZmVkZXJhdGVkQXNzZXJ0aW9ucyI6e30sImF1ZCI6ImFwaS1ldS52b25hZ2UuY29tIiwiZXhwIjoxNzE3MDkyODY4LCJqdGkiOiJmNDZhYTViOC1hODA2LTRjMzctODQyMS02OGYwMzJjNDlhMWYiLCJpYXQiOjE3MTcwOTE5NzAsImlzcyI6IlZJQU0tSUFQIiwibmJmIjoxNzE3MDkxOTU1fQ.iLUbyDPR1HGLKh29fy6fqK65Q1O7mjWOletAEPJD4eu7gb0E85EL4M9R7ckJq5lIvgedQt3vBheTaON9_u-VYjMqo8ulPoEoGUDHbOzNbs4MmCW0_CRdDPGyxnUhvcbuJhPgnEHxmfHjJBljncUnk-Z7XCgyNajBNXeQQnHkRF_6NMngxJ-qjjhqbYL0VsF_JS7-TXxixNL0KAFl0SeN2DjkfwRBCclP-69CTExDjyOvouAcchqi-6ZYj_tXPCrTADuzUrQrW8C5nHp2-XjWJSFKzyvi48n8V1U6KseV-eYzBzvy7bJf0tRMX7G6gctTYq3DxdC_eXvXlnp1zx16mg'
    )

    stub(
        responses.POST,
        'https://api-eu.vonage.com/camara/number-verification/v031/verify',
        fixture_path='number_verification/verify.json',
    )
    response = number_verification.verify(access_token, phone_number='447700900000')
    assert response['devicePhoneNumberVerified'] == True

    new_access_token = number_verification.exchange_code_for_token(
        'code', 'https://example.com/callback'
    )
    response = number_verification.verify(new_access_token, hashed_phone_number='hash')
    assert response['devicePhoneNumberVerified'] == True


def test_verify_error_if_both_phone_number_and_hashed_phone_number_provided(
    number_verification: NumberVerification,
):
    with raises(
        NumberVerificationError,
        match='Only one of "phone_number" and "hashed_phone_number" can be provided.',
    ):
        number_verification.verify(
            access_token='asdf', phone_number='447700900000', hashed_phone_number='hash'
        )
