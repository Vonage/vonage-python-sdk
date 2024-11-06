# Vonage Subaccount Package

This package contains the code to use Vonage's Subaccount API in Python.

It includes methods for creating and modifying Vonage subaccounts and transferring credit, balances and numbers between subaccounts.

## Usage

It is recommended to use this as part of the main `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`.


### List Subaccounts

```python
response = vonage_client.subaccounts.list_subaccounts()
print(response.model_dump)
```

### Create Subaccount

```python
from vonage_subaccounts import SubaccountOptions

response = vonage_client.subaccounts.create_subaccount(
    SubaccountOptions(
        name='test_subaccount', secret='1234asdfA', use_primary_account_balance=False
    )
)
print(response)
```

### Modify a Subaccount

```python
from vonage_subaccounts import ModifySubaccountOptions

response = vonage_client.subaccounts.modify_subaccount(
    'test_subaccount',
    ModifySubaccountOptions(
        suspended=True,
        name='modified_test_subaccount',
    ),
)
print(response)
```

### List Balance Transfers

```python
from vonage_subaccounts import ListTransfersFilter

filter = {'start_date': '2023-08-07T10:50:44Z'}
response = vonage_client.subaccounts.list_balance_transfers(ListTransfersFilter(**filter))
for item in response:
    print(item.model_dump())
```

### Transfer Balance Between Subaccounts

```python
from vonage_subaccounts import TransferRequest

request = TransferRequest(
    from_='test_api_key', to='test_subaccount', amount=0.02, reference='A reference'
)
response = vonage_client.subaccounts.transfer_balance(request)
print(response)
```

### List Credit Transfers

```python
from vonage_subaccounts import ListTransfersFilter

filter = {'start_date': '2023-08-07T10:50:44Z'}
response = vonage_client.subaccounts.list_credit_transfers(ListTransfersFilter(**filter))
for item in response:
    print(item.model_dump())
```

### Transfer Credit Between Subaccounts

```python
from vonage_subaccounts import TransferRequest

request = TransferRequest(
    from_='test_api_key', to='test_subaccount', amount=0.02, reference='A reference'
)
response = vonage_client.subaccounts.transfer_balance(request)
print(response)
```

### Transfer a Phone Number Between Subaccounts

```python
from vonage_subaccounts import TransferNumberRequest

request = TransferNumberRequest(
    from_='test_api_key', to='test_subaccount', number='447700900000', country='GB'
)
response = vonage_client.subaccounts.transfer_number(request)
print(response)
```