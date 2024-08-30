from os.path import abspath

import responses
from pytest import raises
from vonage_http_client.errors import ForbiddenError
from vonage_http_client.http_client import HttpClient
from vonage_subaccounts.errors import InvalidSecretError
from vonage_subaccounts.requests import (
    ListTransfersFilter,
    SubaccountOptions,
    TransferNumberRequest,
    TransferRequest,
)
from vonage_subaccounts.subaccounts import Subaccounts

from testutils import build_response, get_mock_api_key_auth

path = abspath(__file__)

subaccounts = Subaccounts(HttpClient(get_mock_api_key_auth()))


def test_http_client_property():
    http_client = subaccounts.http_client
    assert isinstance(http_client, HttpClient)


@responses.activate
def test_list_subaccounts():
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/accounts/test_api_key/subaccounts',
        'list_subaccounts.json',
    )
    response = subaccounts.list_subaccounts()

    assert response.primary_account.api_key == 'test_api_key'
    assert response.primary_account.name == 'SMPP Account'
    assert response.primary_account.created_at == '2024-08-28T02:02:14.626Z'
    assert response.primary_account.suspended is False

    assert len(response.subaccounts) == 2
    assert response.subaccounts[0].api_key == 'qwer1234'
    assert response.subaccounts[0].name == 'second own balance subacct'
    assert response.subaccounts[0].primary_account_api_key == 'test_api_key'
    assert response.subaccounts[0].use_primary_account_balance is False

    assert response.total_balance == 29.6672
    assert response.total_credit_limit == 0


@responses.activate
def test_create_subaccount():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/accounts/test_api_key/subaccounts',
        'create_subaccount.json',
    )

    response = subaccounts.create_subaccount(
        SubaccountOptions(
            name='test_subaccount', secret='1234asdfA', use_primary_account_balance=False
        )
    )

    assert response.api_key == '1234qwer'
    assert response.secret == 'SuperSecr3t'
    assert response.name == 'test_subaccount'
    assert response.suspended is False
    assert response.use_primary_account_balance is False


@responses.activate
def test_get_subaccount():
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/accounts/test_api_key/subaccounts/1234qwer',
        'get_subaccount.json',
    )

    response = subaccounts.get_subaccount('1234qwer')

    assert response.api_key == '1234qwer'
    assert response.name == 'test_subaccount'
    assert response.suspended is False
    assert response.use_primary_account_balance is False


@responses.activate
def test_modify_subaccount():
    build_response(
        path,
        'PATCH',
        'https://api.nexmo.com/accounts/test_api_key/subaccounts/1234qwer',
        'modify_subaccount.json',
    )

    response = subaccounts.modify_subaccount(
        '1234qwer',
        {
            'suspended': True,
            'name': 'modified_test_subaccount',
        },
    )

    assert response.api_key == '1234qwer'
    assert response.name == 'modified_test_subaccount'
    assert response.suspended is True
    assert response.use_primary_account_balance is False


@responses.activate
def test_list_balance_transfers():
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/accounts/test_api_key/balance-transfers',
        'list_balance_transfers.json',
    )

    response = subaccounts.list_balance_transfers(
        ListTransfersFilter(start_date='2023-08-07T10:50:44Z')
    )

    assert len(response) == 2
    assert response[0].id == '6917b0ae-aed3-453c-a918-e37f6ef7b21a'
    assert response[0].amount == 0.01
    assert response[1].from_ == 'test_api_key'
    assert response[1].to == 'asdfqwer'
    assert response[1].created_at == '2023-12-22T19:40:36.000Z'


@responses.activate
def test_transfer_balance():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/accounts/test_api_key/balance-transfers',
        'transfer.json',
    )

    request = TransferRequest(
        from_='test_api_key', to='asdfqwer', amount=0.02, reference='A reference'
    )
    response = subaccounts.transfer_balance(request)

    assert response.id == 'a1a90387-fcf2-41dc-9beb-cfd82b6b994d'
    assert response.amount == 0.02
    assert response.from_ == 'test_api_key'
    assert response.to == 'asdfqwer'
    assert response.reference == 'A reference'


@responses.activate
def test_list_credit_transfers():
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/accounts/test_api_key/credit-transfers',
        'list_credit_transfers.json',
    )

    response = subaccounts.list_credit_transfers(
        ListTransfersFilter(start_date='2023-08-07T10:50:44Z')
    )

    assert len(response) == 2
    assert response[0].id == '6917b0ae-aed3-453c-a918-e37f6ef7b21a'
    assert response[0].amount == 0.01
    assert response[1].from_ == 'test_api_key'
    assert response[1].to == 'asdfqwer'
    assert response[1].created_at == '2023-12-22T19:40:36.000Z'


@responses.activate
def test_transfer_credit():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/accounts/test_api_key/credit-transfers',
        'transfer.json',
    )

    request = TransferRequest(
        from_='test_api_key', to='asdfqwer', amount=0.02, reference='A reference'
    )
    response = subaccounts.transfer_credit(request)

    assert response.id == 'a1a90387-fcf2-41dc-9beb-cfd82b6b994d'
    assert response.amount == 0.02
    assert response.from_ == 'test_api_key'
    assert response.to == 'asdfqwer'
    assert response.reference == 'A reference'


@responses.activate
def test_transfer_number():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/accounts/test_api_key/transfer-number',
        'transfer_number.json',
    )

    request = TransferNumberRequest(
        from_='test_api_key', to='asdfqwer', number='447700900000', country='GB'
    )
    response = subaccounts.transfer_number(request)

    assert response.number == '447700900000'
    assert response.country == 'GB'
    assert response.from_ == 'test_api_key'
    assert response.to == 'asdfqwer'


@responses.activate
def test_transfer_number_error_suspended_account():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/accounts/test_api_key/transfer-number',
        'transfer_number_error_suspended_account.json',
        status_code=403,
    )

    request = TransferNumberRequest(
        from_='test_api_key', to='asdfqwer', number='447700900000', country='GB'
    )

    with raises(ForbiddenError) as e:
        subaccounts.transfer_number(request)

    assert 'Invalid Number Transfer' in str(e.value)


def test_invalid_secret():
    with raises(InvalidSecretError):
        subaccounts.create_subaccount(
            SubaccountOptions(name='test_subaccount', secret='asDF1')
        )
    with raises(InvalidSecretError):
        subaccounts.create_subaccount(
            SubaccountOptions(name='test_subaccount', secret='1234asdf')
        )
    with raises(InvalidSecretError):
        subaccounts.create_subaccount(
            SubaccountOptions(name='test_subaccount', secret='1234ASDF')
        )
    with raises(InvalidSecretError):
        subaccounts.create_subaccount(
            SubaccountOptions(name='test_subaccount', secret='asdfASDF')
        )
