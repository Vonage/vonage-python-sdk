# Vonage Utils Package

This package contains utility code that is used by the Vonage Python SDK and other related packages.

The utils module provides two utility functions: `format_phone_number` and `remove_none_values`. It also exposes the `VonageError` type that other exceptions related to Vonage SDK inherit from. This can also be accessed via the main SDK module with `vonage.VonageError`.

## Usage

```python
from utils import format_phone_number, remove_none_values

# Use format_phone_number
try:
    formatted_number = format_phone_number('123-456-7890')
    print(formatted_number)
except (InvalidPhoneNumberError, InvalidPhoneNumberTypeError) as e:
    print(e)

# Use remove_none_values to remove null values from a Vonage API response when converting to a dictionary with the `asdict` method
from dataclasses import asdict

vonage_api_response = vonage.api.method()
cleaned_dict = asdict(my_dataclass, dict_factory=remove_none_values)
print(cleaned_dict)
```