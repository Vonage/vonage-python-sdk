from vonage import Client, ClientError, SubaccountsError
from util import stub

from pytest import raises
import responses

api_key = '1234asdf'
api_secret = 'qwerasdfzxcv'
client = Client(key=api_key, secret=api_secret)
subaccount_key = 'asdfzxcv'


@responses.activate
def test_list_subaccounts():
    stub(
        responses.GET,
        f'https://api.nexmo.com/accounts/{api_key}/subaccounts',
        fixture_path='subaccounts/list_subaccounts.json',
    )
    subaccount_list = client.subaccounts.list_subaccounts()
    assert subaccount_list['total_balance'] == 9.9999
    assert subaccount_list['_embedded']['primary_account']['api_key'] == api_key
    assert subaccount_list['_embedded']['primary_account']['balance'] == 9.9999
    assert subaccount_list['_embedded']['subaccounts'][0]['api_key'] == 'qwerasdf'
    assert subaccount_list['_embedded']['subaccounts'][0]['name'] == 'test_subaccount'


@responses.activate
def test_list_subaccounts_error_authentication():
    stub(
        responses.GET,
        f'https://api.nexmo.com/accounts/{api_key}/subaccounts',
        fixture_path='subaccounts/invalid_credentials.json',
        status_code=401,
    )
    with raises(ClientError) as err:
        client.subaccounts.list_subaccounts()
    assert str(err.value) == 'Authentication failed.'


@responses.activate
def test_list_subaccounts_error_forbidden():
    stub(
        responses.GET,
        f'https://api.nexmo.com/accounts/{api_key}/subaccounts',
        fixture_path='subaccounts/forbidden.json',
        status_code=403,
    )
    with raises(ClientError) as err:
        client.subaccounts.list_subaccounts()
    assert (
        str(err.value)
        == 'Authorisation error: Account 1234adsf is not provisioned to access Subaccount Provisioning API (https://developer.nexmo.com/api-errors#unprovisioned)'
    )


@responses.activate
def test_list_subaccounts_error_not_found():
    stub(
        responses.GET,
        f'https://api.nexmo.com/accounts/{api_key}/subaccounts',
        fixture_path='subaccounts/not_found.json',
        status_code=404,
    )
    with raises(ClientError) as err:
        client.subaccounts.list_subaccounts()
    assert (
        str(err.value)
        == "Invalid API Key: API key '1234asdf' does not exist, or you do not have access (https://developer.nexmo.com/api-errors#invalid-api-key)"
    )


@responses.activate
def test_create_subaccount():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/subaccounts',
        fixture_path='subaccounts/subaccount.json',
    )
    subaccount = client.subaccounts.create_subaccount(
        name='my subaccount', secret='Password123', use_primary_account_balance=True
    )
    assert subaccount['api_key'] == 'asdfzxcv'
    assert subaccount['secret'] == 'Password123'
    assert subaccount['primary_account_api_key'] == api_key
    assert subaccount['use_primary_account_balance'] == True


@responses.activate
def test_create_subaccount_error_authentication():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/subaccounts',
        fixture_path='subaccounts/invalid_credentials.json',
        status_code=401,
    )

    with raises(ClientError) as err:
        client.subaccounts.create_subaccount('failed subaccount')
    assert str(err.value) == 'Authentication failed.'


@responses.activate
def test_create_subaccount_error_forbidden():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/subaccounts',
        fixture_path='subaccounts/forbidden.json',
        status_code=403,
    )

    with raises(ClientError) as err:
        client.subaccounts.create_subaccount('failed subaccount')
    assert (
        str(err.value)
        == 'Authorisation error: Account 1234adsf is not provisioned to access Subaccount Provisioning API (https://developer.nexmo.com/api-errors#unprovisioned)'
    )


@responses.activate
def test_create_subaccount_error_not_found():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/subaccounts',
        fixture_path='subaccounts/not_found.json',
        status_code=404,
    )

    with raises(ClientError) as err:
        client.subaccounts.create_subaccount('failed subaccount')
    assert (
        str(err.value)
        == "Invalid API Key: API key '1234asdf' does not exist, or you do not have access (https://developer.nexmo.com/api-errors#invalid-api-key)"
    )


def test_create_subaccount_error_non_boolean():
    with raises(SubaccountsError) as err:
        client.subaccounts.create_subaccount(
            'failed subaccount', use_primary_account_balance='yes please'
        )
    assert (
        str(err.value)
        == 'If providing a value, it needs to be a boolean. You provided: "yes please"'
    )


@responses.activate
def test_get_subaccount():
    stub(
        responses.GET,
        f'https://api.nexmo.com/accounts/{api_key}/subaccounts/{subaccount_key}',
        fixture_path='subaccounts/subaccount.json',
    )
    subaccount = client.subaccounts.get_subaccount(subaccount_key)
    assert subaccount['api_key'] == 'asdfzxcv'
    assert subaccount['secret'] == 'Password123'
    assert subaccount['primary_account_api_key'] == api_key
    assert subaccount['use_primary_account_balance'] == True


@responses.activate
def test_get_subaccount_error_authentication():
    stub(
        responses.GET,
        f'https://api.nexmo.com/accounts/{api_key}/subaccounts/{subaccount_key}',
        fixture_path='subaccounts/invalid_credentials.json',
        status_code=401,
    )
    with raises(ClientError) as err:
        client.subaccounts.get_subaccount(subaccount_key)
    assert str(err.value) == 'Authentication failed.'


@responses.activate
def test_get_subaccount_error_forbidden():
    stub(
        responses.GET,
        f'https://api.nexmo.com/accounts/{api_key}/subaccounts/{subaccount_key}',
        fixture_path='subaccounts/forbidden.json',
        status_code=403,
    )
    with raises(ClientError) as err:
        client.subaccounts.get_subaccount(subaccount_key)
    assert (
        str(err.value)
        == 'Authorisation error: Account 1234adsf is not provisioned to access Subaccount Provisioning API (https://developer.nexmo.com/api-errors#unprovisioned)'
    )


@responses.activate
def test_get_subaccount_error_not_found():
    stub(
        responses.GET,
        f'https://api.nexmo.com/accounts/{api_key}/subaccounts/{subaccount_key}',
        fixture_path='subaccounts/not_found.json',
        status_code=404,
    )
    with raises(ClientError) as err:
        client.subaccounts.get_subaccount(subaccount_key)
    assert (
        str(err.value)
        == "Invalid API Key: API key '1234asdf' does not exist, or you do not have access (https://developer.nexmo.com/api-errors#invalid-api-key)"
    )
