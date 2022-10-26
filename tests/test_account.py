import platform

from util import *

import vonage
from vonage.errors import PricingTypeError


@responses.activate
def test_get_balance(account, dummy_data):
    stub(responses.GET, "https://rest.nexmo.com/account/get-balance")

    assert isinstance(account.get_balance(), dict)
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_application_info_options(dummy_data):
    app_name, app_version = "ExampleApp", "X.Y.Z"

    stub(responses.GET, "https://rest.nexmo.com/account/get-balance")

    client = vonage.Client(
        key=dummy_data.api_key,
        secret=dummy_data.api_secret,
        app_name=app_name,
        app_version=app_version,
    )
    user_agent = f"vonage-python/{vonage.__version__} python/{platform.python_version()} {app_name}/{app_version}"

    account = client.account
    assert isinstance(account.get_balance(), dict)
    assert request_user_agent() == user_agent


@responses.activate
def test_get_country_pricing(account, dummy_data):
    stub(responses.GET, "https://rest.nexmo.com/account/get-pricing/outbound/sms")

    assert isinstance(account.get_country_pricing("GB"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "country=GB" in request_query()


@responses.activate
def test_get_all_countries_pricing(account, dummy_data):
    stub(responses.GET, "https://rest.nexmo.com/account/get-full-pricing/outbound/sms")

    assert isinstance(account.get_all_countries_pricing(), dict)
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_get_prefix_pricing(account, dummy_data):
    stub(responses.GET, "https://rest.nexmo.com/account/get-prefix-pricing/outbound/sms")

    assert isinstance(account.get_prefix_pricing(44), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "prefix=44" in request_query()


@responses.activate
def test_get_sms_pricing(account, dummy_data):
    stub(responses.GET, "https://rest.nexmo.com/account/get-phone-pricing/outbound/sms")

    assert isinstance(account.get_sms_pricing("447525856424"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "phone=447525856424" in request_query()


@responses.activate
def test_get_voice_pricing(account, dummy_data):
    stub(
        responses.GET, "https://rest.nexmo.com/account/get-phone-pricing/outbound/voice"
    )

    assert isinstance(account.get_voice_pricing("447525856424"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "phone=447525856424" in request_query()


def test_invalid_pricing_type_throws_error(account):
    with pytest.raises(PricingTypeError):
        account.get_country_pricing('GB', 'not_a_valid_pricing_type')


@responses.activate
def test_update_default_sms_webhook(account, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/account/settings")

    params = {"moCallBackUrl": "http://example.com/callback"}

    assert isinstance(account.update_default_sms_webhook(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "moCallBackUrl=http%3A%2F%2Fexample.com%2Fcallback" in request_body()


@responses.activate
def test_topup(account, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/account/top-up")

    params = {"trx": "00X123456Y7890123Z"}

    assert isinstance(account.topup(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "trx=00X123456Y7890123Z" in request_body()


@responses.activate
def test_list_secrets(account):
    stub(
        responses.GET,
        "https://api.nexmo.com/accounts/myaccountid/secrets",
        fixture_path="account/secret_management/list.json",
    )

    secrets = account.list_secrets("myaccountid")
    assert_basic_auth()
    assert secrets["_embedded"]["secrets"][0]["id"] == "ad6dc56f-07b5-46e1-a527-85530e625800"


@responses.activate
def test_list_secrets_missing(account):
    stub(
        responses.GET,
        "https://api.nexmo.com/accounts/myaccountid/secrets",
        status_code=404,
        fixture_path="account/secret_management/missing.json",
    )

    with pytest.raises(vonage.ClientError) as ce:
        account.list_secrets("myaccountid")
    assert_basic_auth()
    assert (
        str(ce.value) == """Invalid API Key: API key 'ABC123' does not exist, or you do not have access (https://developer.nexmo.com/api-errors#invalid-api-key)"""
    )


@responses.activate
def test_get_secret(account):
    stub(
        responses.GET,
        "https://api.nexmo.com/accounts/meaccountid/secrets/mahsecret",
        fixture_path="account/secret_management/get.json",
    )

    secret = account.get_secret("meaccountid", "mahsecret")
    assert_basic_auth()
    assert secret["id"] == "ad6dc56f-07b5-46e1-a527-85530e625800"


@responses.activate
def test_create_secret(account):
    stub(
        responses.POST,
        "https://api.nexmo.com/accounts/meaccountid/secrets",
        fixture_path="account/secret_management/create.json",
    )

    secret = account.create_secret("meaccountid", "mahsecret")
    assert_basic_auth()
    assert secret["id"] == "ad6dc56f-07b5-46e1-a527-85530e625800"


@responses.activate
def test_create_secret_max_secrets(account):
    stub(
        responses.POST,
        "https://api.nexmo.com/accounts/meaccountid/secrets",
        status_code=403,
        fixture_path="account/secret_management/max-secrets.json",
    )

    with pytest.raises(vonage.ClientError) as ce:
        account.create_secret("meaccountid", "mahsecret")
    assert_basic_auth()
    assert (
        str(ce.value) == """Maxmimum number of secrets already met: This account has reached maximum number of '2' allowed secrets (https://developer.nexmo.com/api-errors/account/secret-management#maximum-secrets-allowed)"""
    )


@responses.activate
def test_create_secret_validation(account):
    stub(
        responses.POST,
        "https://api.nexmo.com/accounts/meaccountid/secrets",
        status_code=400,
        fixture_path="account/secret_management/create-validation.json",
    )

    with pytest.raises(vonage.ClientError) as ce:
        account.create_secret("meaccountid", "mahsecret")
    assert_basic_auth()
    assert (
        str(ce.value) == """Bad Request: The request failed due to validation errors (https://developer.nexmo.com/api-errors/account/secret-management#validation)"""
    )


@responses.activate
def test_delete_secret(account):
    stub(
        responses.DELETE, "https://api.nexmo.com/accounts/meaccountid/secrets/mahsecret"
    )

    account.revoke_secret("meaccountid", "mahsecret")
    assert_basic_auth()


@responses.activate
def test_delete_secret_last_secret(account):
    stub(
        responses.DELETE,
        "https://api.nexmo.com/accounts/meaccountid/secrets/mahsecret",
        status_code=403,
        fixture_path="account/secret_management/last-secret.json",
    )
    with pytest.raises(vonage.ClientError) as ce:
        account.revoke_secret("meaccountid", "mahsecret")
    assert_basic_auth()
    assert (
        str(ce.value) == """Secret Deletion Forbidden: Can not delete the last secret. The account must always have at least 1 secret active at any time (https://developer.nexmo.com/api-errors/account/secret-management#delete-last-secret)"""
    )
