# Vonage Account Package

This package contains the code to use Vonage's Account API in Python.

It includes methods for managing Vonage accounts.

## Usage

It is recommended to use this as part of the main `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`.


### Get Account Balance

```python
balance = vonage_client.account.get_balance()
print(balance)
```

### Top-Up Account

```python
response = vonage_client.account.top_up(trx='1234567890')
print(response)
```

### Update the Default SMS Webhook

This will return a Pydantic object (`SettingsResponse`) containing multiple settings for your account.

```python
settings: SettingsResponse = vonage_client.account.update_default_sms_webhook(
    mo_callback_url='https://example.com/inbound_sms_webhook',
    dr_callback_url='https://example.com/delivery_receipt_webhook',
)

print(settings)
```

### List Secrets Associated with the Account

```python
response = vonage_client.account.list_secrets()
print(response)
```

### Create a New Account Secret

```python
secret = vonage_client.account.create_secret('Mytestsecret12345')
print(secret)
```

### Get Information About One Secret

```python
secret = vonage_client.account.get_secret(MY_SECRET_ID)
print(secret)
```

### Revoke a Secret

Note: it isn't possible to revoke all account secrets, there must always be one valid secret. Attempting to do so will give a 403 error.

```python
client.account.revoke_secret(MY_SECRET_ID)
```
