# Vonage Numbers Package

This package contains the code to use Vonage's Numbers API in Python.

It includes methods for managing and buying numbers.

## Usage

It is recommended to use this as part of the main `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`.

### List Numbers You Own

```python
numbers, count, next_page = vonage_client.numbers.list_owned_numbers()
print(numbers)
print(count)
print(next_page)

# With filtering
from vonage_numbers import ListOwnedNumbersFilter
numbers, count, next_page = vonage_client.numbers.list_owned_numbers(
    ListOwnedNumbersFilter(country='GB', size=3, index=2)
)

numbers, count, next_page_index = vonage_client.numbers.list_owned_numbers()
print(numbers)
print(count)
print(next_page_index)
```

### Search for Available Numbers

```python
from vonage_numbers import SearchAvailableNumbersFilter

numbers, count, next_page_index = vonage_client.numbers.search_available_numbers(
    SearchAvailableNumbersFilter(
        country='GB', size=10, pattern='44701', search_pattern=1
    )
)
print(numbers)
print(count)
print(next_page_index)
```

### Buy a Number

```python
from vonage_numbers import NumberParams

status = vonage_client.numbers.buy_number(NumberParams(country='GB', msisdn='447007000000'))
print(status)
```

### Cancel a number

```python
from vonage_numbers import NumberParams

status = vonage_client.numbers.cancel_number(NumberParams(country='GB', msisdn='447007000000'))
print(status)
```

### Update a Number

```python
from vonage_numbers import UpdateNumberParams

status = vonage_client.numbers.update_number(
    UpdateNumberParams(
        country='GB',
        msisdn='447007000000',
        mo_http_url='https://example.com',
        mo_smpp_sytem_type='inbound',
        voice_callback_type='tel',
        voice_callback_value='447008000000',
        voice_status_callback='https://example.com',
    )
)

print(status)
```