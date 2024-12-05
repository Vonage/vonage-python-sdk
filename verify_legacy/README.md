# Vonage Legacy Verify Package

This package contains the code to use Vonage's legacy Verify API in Python. This package includes methods for working with 2-factor authentication (2FA) messages sent via SMS or TTS.

Note: There is a more current package available: [Vonage's Verify API](https://developer.vonage.com/en/verify/overview), which is recommended for most use cases. The newer API lets you send messages via multiple channels, including Email, SMS, MMS, WhatsApp, Messenger and others. You can also make Silent Authentication requests with the new Verify package to give an end user a more seamless experience.

## Usage

It is recommended to use this as part of the main `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`.

### Make a Verify Request

```python
from vonage_verify_legacy import VerifyRequest
params = {'number': '1234567890', 'brand': 'Acme Inc.'}
request = VerifyRequest(**params)
response = vonage_client.verify_legacy.start_verification(request)
```

### Make a PSD2 (Payment Services Directive v2) Request

```python
from vonage_verify_legacy import Psd2Request
params = {'number': '1234567890', 'payee': 'Acme Inc.', 'amount': 99.99}
request = VerifyRequest(**params)
response = vonage_client.verify_legacy.start_verification(request)
```

### Check a Verification Code

```python
vonage_client.verify_legacy.check_code(request_id='my_request_id', code='1234')
```

### Search Verification Requests

```python
# Search for single request
response = vonage_client.verify_legacy.search('my_request_id')

# Search for multiple requests
response = vonage_client.verify_legacy.search(['my_request_id_1', 'my_request_id_2'])
```

### Cancel a Verification

```python
response = vonage_client.verify_legacy.cancel_verification('my_request_id')
```

### Trigger the Next Workflow Event

```python
response = vonage_client.verify_legacy.trigger_next_event('my_request_id')
```

### Request a Network Unblock

Note: Network Unblock is switched off by default. Contact Sales to enable the Network Unblock API for your account.

```python
response = vonage_client.verify_legacy.request_network_unblock('23410')
```