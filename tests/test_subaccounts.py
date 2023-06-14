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
    subaccounts = client.subaccounts.list_subaccounts()
    assert subaccounts['total_balance'] == 9.9999
    assert subaccounts['_embedded']['primary_account']['api_key'] == api_key
    assert subaccounts['_embedded']['primary_account']['balance'] == 9.9999
    assert subaccounts['_embedded']['subaccounts'][0]['api_key'] == 'qwerasdf'
    assert subaccounts['_embedded']['subaccounts'][0]['name'] == 'test_subaccount'


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


@responses.activate
def test_modify_subaccount():
    stub(
        responses.PATCH,
        f'https://api.nexmo.com/accounts/{api_key}/subaccounts/{subaccount_key}',
        fixture_path='subaccounts/modified_subaccount.json',
    )
    subaccount = client.subaccounts.modify_subaccount(
        subaccount_key,
        suspended=True,
        use_primary_account_balance=False,
        name='my modified subaccount',
    )
    assert subaccount['api_key'] == 'asdfzxcv'
    assert subaccount['name'] == 'my modified subaccount'
    assert subaccount['suspended'] == True
    assert subaccount['primary_account_api_key'] == api_key
    assert subaccount['use_primary_account_balance'] == False


@responses.activate
def test_modify_subaccount_error_authentication():
    stub(
        responses.PATCH,
        f'https://api.nexmo.com/accounts/{api_key}/subaccounts/{subaccount_key}',
        fixture_path='subaccounts/invalid_credentials.json',
        status_code=401,
    )
    with raises(ClientError) as err:
        client.subaccounts.modify_subaccount(subaccount_key, suspended=True)
    assert str(err.value) == 'Authentication failed.'


@responses.activate
def test_modify_subaccount_error_forbidden():
    stub(
        responses.PATCH,
        f'https://api.nexmo.com/accounts/{api_key}/subaccounts/{subaccount_key}',
        fixture_path='subaccounts/forbidden.json',
        status_code=403,
    )
    with raises(ClientError) as err:
        client.subaccounts.modify_subaccount(subaccount_key, use_primary_account_balance=False)
    assert (
        str(err.value)
        == 'Authorisation error: Account 1234adsf is not provisioned to access Subaccount Provisioning API (https://developer.nexmo.com/api-errors#unprovisioned)'
    )


@responses.activate
def test_modify_subaccount_error_not_found():
    stub(
        responses.PATCH,
        f'https://api.nexmo.com/accounts/{api_key}/subaccounts/{subaccount_key}',
        fixture_path='subaccounts/not_found.json',
        status_code=404,
    )
    with raises(ClientError) as err:
        client.subaccounts.modify_subaccount(subaccount_key, name='my modified subaccount name')
    assert (
        str(err.value)
        == "Invalid API Key: API key '1234asdf' does not exist, or you do not have access (https://developer.nexmo.com/api-errors#invalid-api-key)"
    )


@responses.activate
def test_modify_subaccount_validation_error():
    stub(
        responses.PATCH,
        f'https://api.nexmo.com/accounts/{api_key}/subaccounts/{subaccount_key}',
        fixture_path='subaccounts/validation_error.json',
        status_code=422,
    )
    with raises(ClientError) as err:
        client.subaccounts.modify_subaccount(subaccount_key, use_primary_account_balance=True)
    assert (
        str(err.value)
        == 'Bad Request: The request failed due to validation errors (https://developer.nexmo.com/api-errors/account/subaccounts#validation)'
    )


@responses.activate
def test_list_credit_transfers():
    stub(
        responses.GET,
        f'https://api.nexmo.com/accounts/{api_key}/credit-transfers',
        fixture_path='subaccounts/list_credit_transfers.json',
    )
    transfers = client.subaccounts.list_credit_transfers(
        start_date='2022-03-29T14:16:56Z',
        end_date='2023-06-12T17:20:01Z',
        subaccount='asdfzxcv',
    )
    assert transfers['_embedded']['credit_transfers'][0]['from'] == '1234asdf'
    assert transfers['_embedded']['credit_transfers'][0]['reference'] == 'test credit transfer'
    assert transfers['_embedded']['credit_transfers'][1]['to'] == 'asdfzxcv'
    assert transfers['_embedded']['credit_transfers'][1]['created_at'] == '2023-06-12T17:20:01.000Z'


@responses.activate
def test_list_credit_transfers_error_authentication():
    stub(
        responses.GET,
        f'https://api.nexmo.com/accounts/{api_key}/credit-transfers',
        fixture_path='subaccounts/invalid_credentials.json',
        status_code=401,
    )

    with raises(ClientError) as err:
        client.subaccounts.list_credit_transfers()
    assert str(err.value) == 'Authentication failed.'


@responses.activate
def test_list_credit_transfers_error_forbidden():
    stub(
        responses.GET,
        f'https://api.nexmo.com/accounts/{api_key}/credit-transfers',
        fixture_path='subaccounts/forbidden.json',
        status_code=403,
    )
    with raises(ClientError) as err:
        client.subaccounts.list_credit_transfers()
    assert (
        str(err.value)
        == 'Authorisation error: Account 1234adsf is not provisioned to access Subaccount Provisioning API (https://developer.nexmo.com/api-errors#unprovisioned)'
    )


@responses.activate
def test_list_credit_transfers_error_not_found():
    stub(
        responses.GET,
        f'https://api.nexmo.com/accounts/{api_key}/credit-transfers',
        fixture_path='subaccounts/not_found.json',
        status_code=404,
    )

    with raises(ClientError) as err:
        client.subaccounts.list_credit_transfers()
    assert (
        str(err.value)
        == "Invalid API Key: API key '1234asdf' does not exist, or you do not have access (https://developer.nexmo.com/api-errors#invalid-api-key)"
    )


@responses.activate
def test_list_credit_transfers_validation_error():
    stub(
        responses.GET,
        f'https://api.nexmo.com/accounts/{api_key}/credit-transfers',
        fixture_path='subaccounts/transfer_validation_error.json',
        status_code=422,
    )
    with raises(ClientError) as err:
        client.subaccounts.list_credit_transfers(start_date='invalid-date-format')
    assert (
        str(err.value)
        == 'Bad Request: The request failed due to validation errors (https://developer.nexmo.com/api-errors/account/subaccounts#validation)'
    )


@responses.activate
def test_transfer_credit():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/credit-transfers',
        fixture_path='subaccounts/credit_transfer.json',
    )
    transfer = client.subaccounts.transfer_credit(
        from_='1234asdf', to='asdfzxcv', amount=0.50, reference='test credit transfer'
    )
    assert transfer['from'] == '1234asdf'
    assert transfer['to'] == 'asdfzxcv'
    assert transfer['amount'] == 0.5
    assert transfer['reference'] == 'test credit transfer'


@responses.activate
def test_transfer_credit_error_authentication():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/credit-transfers',
        fixture_path='subaccounts/invalid_credentials.json',
        status_code=401,
    )

    with raises(ClientError) as err:
        client.subaccounts.transfer_credit(from_='1234asdf', to='asdfzxcv', amount=0.1)
    assert str(err.value) == 'Authentication failed.'


@responses.activate
def test_transfer_credit_invalid_transfer():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/credit-transfers',
        fixture_path='subaccounts/invalid_transfer.json',
        status_code=403,
    )
    with raises(ClientError) as err:
        client.subaccounts.transfer_credit(from_='asdfzxcv', to='qwerasdf', amount=1)
    assert (
        str(err.value)
        == 'Invalid Transfer: Transfers are only allowed between a primary account and its subaccount (https://developer.nexmo.com/api-errors/account/subaccounts#valid-transfers)'
    )


@responses.activate
def test_transfer_credit_insufficient_credit():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/credit-transfers',
        fixture_path='subaccounts/insufficient_credit.json',
        status_code=403,
    )
    with raises(ClientError) as err:
        client.subaccounts.transfer_credit(from_='asdfzxcv', to='qwerasdf', amount=1)
    assert (
        str(err.value)
        == 'Transfer amount is invalid: Insufficient Credit (https://developer.nexmo.com/api-errors/account/subaccounts#valid-transfers)'
    )


@responses.activate
def test_transfer_credit_error_not_found():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/credit-transfers',
        fixture_path='subaccounts/not_found.json',
        status_code=404,
    )

    with raises(ClientError) as err:
        client.subaccounts.transfer_credit(from_='1234asdf', to='asdfzcv', amount=0.1)
    assert (
        str(err.value)
        == "Invalid API Key: API key '1234asdf' does not exist, or you do not have access (https://developer.nexmo.com/api-errors#invalid-api-key)"
    )


@responses.activate
def test_transfer_credit_validation_error():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/credit-transfers',
        fixture_path='subaccounts/must_be_number.json',
        status_code=422,
    )
    with raises(ClientError) as err:
        client.subaccounts.transfer_credit(from_='1234asdf', to='asdfzxcv', amount='0.50')
    assert (
        str(err.value)
        == 'Bad Request: The request failed due to validation errors (https://developer.nexmo.com/api-errors/account/subaccounts#validation)'
    )


@responses.activate
def test_list_balance_transfers():
    stub(
        responses.GET,
        f'https://api.nexmo.com/accounts/{api_key}/balance-transfers',
        fixture_path='subaccounts/list_balance_transfers.json',
    )
    transfers = client.subaccounts.list_balance_transfers(
        start_date='2022-03-29T14:16:56Z',
        end_date='2023-06-12T17:20:01Z',
        subaccount='asdfzxcv',
    )
    assert transfers['_embedded']['balance_transfers'][0]['from'] == '1234asdf'
    assert transfers['_embedded']['balance_transfers'][0]['reference'] == 'test transfer'
    assert transfers['_embedded']['balance_transfers'][1]['to'] == 'asdfzxcv'
    assert (
        transfers['_embedded']['balance_transfers'][1]['created_at'] == '2023-06-12T17:20:01.000Z'
    )


@responses.activate
def test_list_balance_transfers_error_authentication():
    stub(
        responses.GET,
        f'https://api.nexmo.com/accounts/{api_key}/balance-transfers',
        fixture_path='subaccounts/invalid_credentials.json',
        status_code=401,
    )

    with raises(ClientError) as err:
        client.subaccounts.list_balance_transfers()
    assert str(err.value) == 'Authentication failed.'


@responses.activate
def test_list_balance_transfers_error_forbidden():
    stub(
        responses.GET,
        f'https://api.nexmo.com/accounts/{api_key}/balance-transfers',
        fixture_path='subaccounts/forbidden.json',
        status_code=403,
    )
    with raises(ClientError) as err:
        client.subaccounts.list_balance_transfers()
    assert (
        str(err.value)
        == 'Authorisation error: Account 1234adsf is not provisioned to access Subaccount Provisioning API (https://developer.nexmo.com/api-errors#unprovisioned)'
    )


@responses.activate
def test_list_balance_transfers_error_not_found():
    stub(
        responses.GET,
        f'https://api.nexmo.com/accounts/{api_key}/balance-transfers',
        fixture_path='subaccounts/not_found.json',
        status_code=404,
    )

    with raises(ClientError) as err:
        client.subaccounts.list_balance_transfers()
    assert (
        str(err.value)
        == "Invalid API Key: API key '1234asdf' does not exist, or you do not have access (https://developer.nexmo.com/api-errors#invalid-api-key)"
    )


@responses.activate
def test_list_balance_transfers_validation_error():
    stub(
        responses.GET,
        f'https://api.nexmo.com/accounts/{api_key}/balance-transfers',
        fixture_path='subaccounts/transfer_validation_error.json',
        status_code=422,
    )
    with raises(ClientError) as err:
        client.subaccounts.list_balance_transfers(start_date='invalid-date-format')
    assert (
        str(err.value)
        == 'Bad Request: The request failed due to validation errors (https://developer.nexmo.com/api-errors/account/subaccounts#validation)'
    )


@responses.activate
def test_transfer_balance():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/balance-transfers',
        fixture_path='subaccounts/balance_transfer.json',
    )
    transfer = client.subaccounts.transfer_balance(
        from_='1234asdf', to='asdfzxcv', amount=0.50, reference='test balance transfer'
    )
    assert transfer['from'] == '1234asdf'
    assert transfer['to'] == 'asdfzxcv'
    assert transfer['amount'] == 0.5
    assert transfer['reference'] == 'test balance transfer'


@responses.activate
def test_transfer_balance_error_authentication():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/balance-transfers',
        fixture_path='subaccounts/invalid_credentials.json',
        status_code=401,
    )

    with raises(ClientError) as err:
        client.subaccounts.transfer_balance(from_='1234asdf', to='asdfzxcv', amount=0.1)
    assert str(err.value) == 'Authentication failed.'


@responses.activate
def test_transfer_balance_invalid_transfer():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/balance-transfers',
        fixture_path='subaccounts/invalid_transfer.json',
        status_code=403,
    )
    with raises(ClientError) as err:
        client.subaccounts.transfer_balance(from_='asdfzxcv', to='qwerasdf', amount=1)
    assert (
        str(err.value)
        == 'Invalid Transfer: Transfers are only allowed between a primary account and its subaccount (https://developer.nexmo.com/api-errors/account/subaccounts#valid-transfers)'
    )


@responses.activate
def test_transfer_balance_error_not_found():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/balance-transfers',
        fixture_path='subaccounts/not_found.json',
        status_code=404,
    )

    with raises(ClientError) as err:
        client.subaccounts.transfer_balance(from_='1234asdf', to='asdfzcv', amount=0.1)
    assert (
        str(err.value)
        == "Invalid API Key: API key '1234asdf' does not exist, or you do not have access (https://developer.nexmo.com/api-errors#invalid-api-key)"
    )


@responses.activate
def test_transfer_balance_validation_error():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/balance-transfers',
        fixture_path='subaccounts/must_be_number.json',
        status_code=422,
    )
    with raises(ClientError) as err:
        client.subaccounts.transfer_balance(from_='1234asdf', to='asdfzxcv', amount='0.50')
    assert (
        str(err.value)
        == 'Bad Request: The request failed due to validation errors (https://developer.nexmo.com/api-errors/account/subaccounts#validation)'
    )


@responses.activate
def test_transfer_number():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/transfer-number',
        fixture_path='subaccounts/transfer_number.json',
    )
    transfer = client.subaccounts.transfer_number(
        from_='1234asdf', to='asdfzxcv', number='12345678901', country='US'
    )
    assert transfer['from'] == '1234asdf'
    assert transfer['to'] == 'asdfzxcv'
    assert transfer['number'] == '12345678901'
    assert transfer['country'] == 'US'
    assert transfer['masterAccountId'] == '1234asdf'


@responses.activate
def test_transfer_number_error_authentication():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/transfer-number',
        fixture_path='subaccounts/invalid_credentials.json',
        status_code=401,
    )

    with raises(ClientError) as err:
        client.subaccounts.transfer_number(
            from_='1234asdf', to='asdfzxcv', number='12345678901', country='US'
        )
    assert str(err.value) == 'Authentication failed.'


@responses.activate
def test_transfer_number_invalid_transfer():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/transfer-number',
        fixture_path='subaccounts/invalid_number_transfer.json',
        status_code=403,
    )
    with raises(ClientError) as err:
        client.subaccounts.transfer_number(
            from_='1234asdf', to='asdfzxcv', number='12345678901', country='US'
        )
    assert (
        str(err.value)
        == 'Invalid Number Transfer: Could not transfer number 12345678901 from account 1234asdf to asdfzxcv - ShortCode is not owned by from account (https://developer.nexmo.com/api-errors/account/subaccounts#invalid-number-transfer)'
    )


@responses.activate
def test_transfer_number_error_number_not_found():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/transfer-number',
        fixture_path='subaccounts/number_not_found.json',
        status_code=404,
    )

    with raises(ClientError) as err:
        client.subaccounts.transfer_number(
            from_='1234asdf', to='asdfzxcv', number='12345678901', country='US'
        )
    assert (
        str(err.value)
        == 'Invalid Number Transfer: Could not transfer number 12345678901 from account 1234asdf to asdfzxcv - ShortCode not found (https://developer.nexmo.com/api-errors/account/subaccounts#missing-number-transfer)'
    )


@responses.activate
def test_transfer_number_error_number_not_found():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/transfer-number',
        fixture_path='subaccounts/number_not_found.json',
        status_code=404,
    )

    with raises(ClientError) as err:
        client.subaccounts.transfer_number(
            from_='1234asdf', to='asdfzxcv', number='12345678901', country='US'
        )
    assert (
        str(err.value)
        == 'Invalid Number Transfer: Could not transfer number 12345678901 from account 1234asdf to asdfzxcv - ShortCode not found (https://developer.nexmo.com/api-errors/account/subaccounts#missing-number-transfer)'
    )


@responses.activate
def test_transfer_number_validation_error():
    stub(
        responses.POST,
        f'https://api.nexmo.com/accounts/{api_key}/transfer-number',
        fixture_path='subaccounts/same_from_and_to_accounts.json',
        status_code=422,
    )
    with raises(ClientError) as err:
        client.subaccounts.transfer_number(
            from_='asdfzxcv', to='asdfzxcv', number='12345678901', country='US'
        )
    assert (
        str(err.value)
        == 'Bad Request: The request failed due to validation errors (https://developer.nexmo.com/api-errors/account/subaccounts#validation)'
    )
