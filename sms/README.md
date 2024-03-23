# Vonage SMS Package

This package contains the code to use Vonage's SMS API in Python.

It includes a method for sending SMS messages and returns an `SmsResponse` class to handle the response.

## Usage

It is recommended to use this as part of the main `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`.

### Send an SMS

Create an `SmsMessage` object, then pass into the `Sms.send` method.

```python
from vonage_sms import SmsMessage, SmsResponse

message = SmsMessage(to='1234567890', from_='Acme Inc.', text='Hello, World!')
response: SmsResponse = vonage_client.sms.send(message)

print(response.model_dump(exclude_unset=True))
```


