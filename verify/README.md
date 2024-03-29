# Vonage Verify Package

This package contains the code to use Vonage's Verify API in Python. There is a more current package to user Vonage's Verify v2 API which is recommended to use for most use cases. The v2 API lets you send messages via multiple channels, including Email, SMS, MMS, WhatsApp, Messenger and others. You can also make Silent Authentication requests with Verify v2 to give an end user a more seamless experience.

This package includes methods for sending 2-factor authentication (2FA) messages and returns...


asdf
asdf


## Usage

It is recommended to use this as part of the main `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`.

### Make a Verify Request

<!-- Create an `SmsMessage` object, then pass into the `Sms.send` method.

```python
from vonage_sms import SmsMessage, SmsResponse

message = SmsMessage(to='1234567890', from_='Acme Inc.', text='Hello, World!')
response: SmsResponse = vonage_client.sms.send(message)

print(response.model_dump(exclude_unset=True))
``` -->
