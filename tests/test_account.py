import platform

from glom import glom

from util import *

import nexmo


@responses.activate
def test_get_balance(client, dummy_data):
    stub(responses.GET, "https://rest.nexmo.com/account/get-balance")

    assert isinstance(client.get_balance(), dict)
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_application_info_options(dummy_data):
    app_name, app_version = "ExampleApp", "X.Y.Z"

    stub(responses.GET, "https://rest.nexmo.com/account/get-balance")

    client = nexmo.Client(
        key=dummy_data.api_key,
        secret=dummy_data.api_secret,
        app_name=app_name,
        app_version=app_version,
    )
    user_agent = "/".join(
        [
            "nexmo-python",
            nexmo.__version__,
            platform.python_version(),
            app_name,
            app_version,
        ]
    )

    assert isinstance(client.get_balance(), dict)
    assert request_user_agent() == user_agent


@responses.activate
def test_get_country_pricing(client, dummy_data):
    stub(responses.GET, "https://rest.nexmo.com/account/get-pricing/outbound")

    assert isinstance(client.get_country_pricing("GB"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "country=GB" in request_query()


@responses.activate
def test_get_prefix_pricing(client, dummy_data):
    stub(responses.GET, "https://rest.nexmo.com/account/get-prefix-pricing/outbound")

    assert isinstance(client.get_prefix_pricing(44), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "prefix=44" in request_query()


@responses.activate
def test_get_sms_pricing(client, dummy_data):
    stub(responses.GET, "https://rest.nexmo.com/account/get-phone-pricing/outbound/sms")

    assert isinstance(client.get_sms_pricing("447525856424"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "phone=447525856424" in request_query()


@responses.activate
def test_get_voice_pricing(client, dummy_data):
    stub(
        responses.GET, "https://rest.nexmo.com/account/get-phone-pricing/outbound/voice"
    )

    assert isinstance(client.get_voice_pricing("447525856424"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "phone=447525856424" in request_query()


@responses.activate
def test_update_settings(client, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/account/settings")

    params = {"moCallBackUrl": "http://example.com/callback"}

    assert isinstance(client.update_settings(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "moCallBackUrl=http%3A%2F%2Fexample.com%2Fcallback" in request_body()


@responses.activate
def test_topup(client, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/account/top-up")

    params = {"trx": "00X123456Y7890123Z"}

    assert isinstance(client.topup(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "trx=00X123456Y7890123Z" in request_body()


@responses.activate
def test_get_account_numbers(client, dummy_data):
    stub(responses.GET, "https://rest.nexmo.com/account/numbers")

    assert isinstance(client.get_account_numbers(size=25), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_params()["size"] == ["25"]


@responses.activate
def test_list_secrets(client):
    stub(
        responses.GET,
        "https://api.nexmo.com/accounts/meaccountid/secrets",
        fixture_path="account/secret_management/list.json",
    )

    secrets = client.list_secrets("meaccountid")
    assert_basic_auth()
    assert (
        glom(secrets, "_embedded.secrets.0.id")
        == "ad6dc56f-07b5-46e1-a527-85530e625800"
    )


@responses.activate
def test_list_secrets_missing(client):
    stub(
        responses.GET,
        "https://api.nexmo.com/accounts/meaccountid/secrets",
        status_code=404,
        fixture_path="account/secret_management/missing.json",
    )

    with pytest.raises(nexmo.ClientError) as ce:
        client.list_secrets("meaccountid")
    assert_basic_auth()
    assert (
        """ClientError: Invalid API Key: API key 'ABC123' does not exist, or you do not have access (https://developer.nexmo.com/api-errors#invalid-api-key)"""
        in str(ce)
    )


@responses.activate
def test_get_secret(client):
    stub(
        responses.GET,
        "https://api.nexmo.com/accounts/meaccountid/secrets/mahsecret",
        fixture_path="account/secret_management/get.json",
    )

    secret = client.get_secret("meaccountid", "mahsecret")
    assert_basic_auth()
    assert secret["id"] == "ad6dc56f-07b5-46e1-a527-85530e625800"


@responses.activate
def test_delete_secret(client):
    stub(
        responses.DELETE, "https://api.nexmo.com/accounts/meaccountid/secrets/mahsecret"
    )

    client.delete_secret("meaccountid", "mahsecret")
    assert_basic_auth()


@responses.activate
def test_delete_secret_last_secret(client):
    stub(
        responses.DELETE,
        "https://api.nexmo.com/accounts/meaccountid/secrets/mahsecret",
        status_code=403,
        fixture_path="account/secret_management/last-secret.json",
    )
    with pytest.raises(nexmo.ClientError) as ce:
        client.delete_secret("meaccountid", "mahsecret")
    assert_basic_auth()
    assert (
        """ClientError: Secret Deletion Forbidden: Can not delete the last secret. The account must always have at least 1 secret active at any time (https://developer.nexmo.com/api-errors/account/secret-management#delete-last-secret)"""
        in str(ce)
    )


@responses.activate
def test_create_secret(client):
    stub(
        responses.POST,
        "https://api.nexmo.com/accounts/meaccountid/secrets",
        fixture_path="account/secret_management/create.json",
    )

    secret = client.create_secret("meaccountid", "mahsecret")
    assert_basic_auth()
    assert secret["id"] == "ad6dc56f-07b5-46e1-a527-85530e625800"


@responses.activate
def test_create_secret_max_secrets(client):
    stub(
        responses.POST,
        "https://api.nexmo.com/accounts/meaccountid/secrets",
        status_code=403,
        fixture_path="account/secret_management/max-secrets.json",
    )

    with pytest.raises(nexmo.ClientError) as ce:
        client.create_secret("meaccountid", "mahsecret")
    assert_basic_auth()
    assert (
        """ClientError: Maxmimum number of secrets already met: This account has reached maximum number of '2' allowed secrets (https://developer.nexmo.com/api-errors/account/secret-management#maximum-secrets-allowed)"""
        in str(ce)
    )


@responses.activate
def test_create_secret_validation(client):
    stub(
        responses.POST,
        "https://api.nexmo.com/accounts/meaccountid/secrets",
        status_code=400,
        fixture_path="account/secret_management/create-validation.json",
    )

    with pytest.raises(nexmo.ClientError) as ce:
        client.create_secret("meaccountid", "mahsecret")
    assert_basic_auth()
    assert (
        """ClientError: Bad Request: The request failed due to validation errors (https://developer.nexmo.com/api-errors/account/secret-management#validation)"""
        in str(ce)
    )
