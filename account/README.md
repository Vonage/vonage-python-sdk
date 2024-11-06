# Vonage Account Package

This package contains the code to use Vonage's Account API in Python.

It includes methods for managing Vonage accounts, managing account secrets and querying country pricing.

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

### Get Service Pricing for a Specific Country

```python
from vonage_account import GetCountryPricingRequest

response = vonage_client.account.get_country_pricing(
    GetCountryPricingRequest(type='sms', country_code='US')
)
print(response)
```

### Get Service Pricing for All Countries

```python
response = vonage_client.account.get_all_countries_pricing(service_type='sms')
print(response)
```

### Get Service Pricing by Dialing Prefix

```python
from vonage_account import GetPrefixPricingRequest

response = client.account.get_prefix_pricing(
    GetPrefixPricingRequest(prefix='44', type='sms')
)
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
