# Vonage Verify V2 Package

This package contains the code to use [Vonage's Verify v2 API](https://developer.vonage.com/en/verify/overview) in Python. This package includes methods for working with 2-factor authentication (2FA) messages sent via SMS, Voice, WhatsApp and Email. You can also make Silent Authentication requests with Verify v2 to give your end user a more seamless experience.

## Usage

It is recommended to use this as part of the main `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`.

### Make a Verify Request

```python
from vonage_verify_v2 import VerifyRequest, SmsChannel
# All channels have associated models
sms_channel = SmsChannel(to='1234567890')
params = {
    'brand': 'Vonage',
    'workflow': [sms_channel],
}
verify_request = VerifyRequest(**params)

response = vonage_client.verify_v2.start_verification(verify_request)
```

If using silent authentication, the response will include a `check_url` field with a url that should be accessed on the user's device to proceed with silent authentication. If used, silent auth must be the first element in the `workflow` list.

```python
silent_auth_channel = SilentAuthChannel(channel=ChannelType.SILENT_AUTH, to='1234567890')
sms_channel = SmsChannel(to='1234567890')
params = {
    'brand': 'Vonage',
    'workflow': [silent_auth_channel, sms_channel],
}
verify_request = VerifyRequest(**params)

response = vonage_client.verify_v2.start_verification(verify_request)
```

### Check a Verification Code

```python
vonage_client.verify_v2.check_code(request_id='my_request_id', code='1234')
```

### Cancel a Verification

```python
vonage_client.verify_v2.cancel_verification('my_request_id')
```

### Trigger the Next Workflow Event

```python
vonage_client.verify_v2.trigger_next_workflow('my_request_id')
```