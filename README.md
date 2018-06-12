Nexmo Client Library for Python
===============================

[![PyPI version](https://badge.fury.io/py/nexmo.svg)](https://badge.fury.io/py/nexmo)
[![Build Status](https://api.travis-ci.org/Nexmo/nexmo-python.svg?branch=master)](https://travis-ci.org/Nexmo/nexmo-python)
[![Coverage Status](https://coveralls.io/repos/github/Nexmo/nexmo-python/badge.svg?branch=master)](https://coveralls.io/github/Nexmo/nexmo-python?branch=master)

This is the Python client library for Nexmo's API. To use it you'll
need a Nexmo account. Sign up [for free at nexmo.com][signup].

* [Installation](#installation)
* [Usage](#usage)
* [SMS API](#sms-api)
* [Voice API](#voice-api)
* [Verify API](#verify-api)
* [Number Insight API](#number-insight-api)
* [Application API](#application-api)
* [Coverage](#api-coverage)
* [License](#license)


Installation
------------

To install the Python client library using pip:

    pip install nexmo

Alternatively you can clone the repository:

    git clone git@github.com:Nexmo/nexmo-python.git


Usage
-----

Begin by importing the `nexmo` module:

```python
import nexmo
```

Then construct a client object with your key and secret:

```python
client = nexmo.Client(key=api_key, secret=api_secret)
```

For production you can specify the `NEXMO_API_KEY` and `NEXMO_API_SECRET`
environment variables instead of specifying the key and secret explicitly.

For newer endpoints that support JWT authentication such as the Voice API,
you can also specify the `application_id` and `private_key` arguments:

```python
client = nexmo.Client(application_id=application_id, private_key=private_key)
```

In order to check signatures for incoming webhook requests, you'll also need
to specify the `signature_secret` argument (or the `NEXMO_SIGNATURE_SECRET`
environment variable).


## SMS API

### Send a text message

```python
response = client.send_message({'from': 'Python', 'to': 'YOUR-NUMBER', 'text': 'Hello world'})

response = response['messages'][0]

if response['status'] == '0':
  print 'Sent message', response['message-id']

  print 'Remaining balance is', response['remaining-balance']
else:
  print 'Error:', response['error-text']
```

Docs: [https://docs.nexmo.com/messaging/sms-api/api-reference#request](https://docs.nexmo.com/messaging/sms-api/api-reference#request?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

### Tell Nexmo the SMS was received

The following submits a successful conversion to Nexmo with the current timestamp. This feature must
be enabled on your account first.

```python
response = client.submit_sms_conversion(message_id)
```


## Voice API

### Make a call

```python
response = client.create_call({
  'to': [{'type': 'phone', 'number': '14843331234'}],
  'from': {'type': 'phone', 'number': '14843335555'},
  'answer_url': ['https://example.com/answer']
})
```

Docs: [https://docs.nexmo.com/voice/voice-api/api-reference#call_create](https://docs.nexmo.com/voice/voice-api/api-reference#call_create?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

### Retrieve a list of calls

```python
response = client.get_calls()
```

Docs: [https://docs.nexmo.com/voice/voice-api/api-reference#call_retrieve](https://docs.nexmo.com/voice/voice-api/api-reference#call_retrieve?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

### Retrieve a single call

```python
response = client.get_call(uuid)
```

Docs: [https://docs.nexmo.com/voice/voice-api/api-reference#call_retrieve_single](https://docs.nexmo.com/voice/voice-api/api-reference#call_retrieve_single?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

### Update a call

```python
response = client.update_call(uuid, action='hangup')
```

Docs: [https://docs.nexmo.com/voice/voice-api/api-reference#call_modify_single](https://docs.nexmo.com/voice/voice-api/api-reference#call_modify_single?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

### Stream audio to a call

```python
stream_url = 'https://nexmo-community.github.io/ncco-examples/assets/voice_api_audio_streaming.mp3'

response = client.send_audio(uuid, stream_url=stream_url)
```

Docs: [https://docs.nexmo.com/voice/voice-api/api-reference#stream_put](https://docs.nexmo.com/voice/voice-api/api-reference#stream_put?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

### Stop streaming audio to a call

```python
response = client.stop_audio(uuid)
```

Docs: [https://docs.nexmo.com/voice/voice-api/api-reference#stream_delete](https://docs.nexmo.com/voice/voice-api/api-reference#stream_delete?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

### Send a synthesized speech message to a call

```python
response = client.send_speech(uuid, text='Hello')
```

Docs: [https://docs.nexmo.com/voice/voice-api/api-reference#talk_put](https://docs.nexmo.com/voice/voice-api/api-reference#talk_put?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

### Stop sending a synthesized speech message to a call

```python
response = client.stop_speech(uuid)
```

Docs: [https://docs.nexmo.com/voice/voice-api/api-reference#talk_delete](https://docs.nexmo.com/voice/voice-api/api-reference#talk_delete?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

### Send DTMF tones to a call

```python
response = client.send_dtmf(uuid, digits='1234')
```

Docs: [https://docs.nexmo.com/voice/voice-api/api-reference#dtmf_put](https://docs.nexmo.com/voice/voice-api/api-reference#dtmf_put?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)


## Verify API

### Start a verification

```python
response = client.start_verification(number='441632960960', brand='MyApp')

if response['status'] == '0':
  print 'Started verification request_id=' + response['request_id']
else:
  print 'Error:', response['error_text']
```

Docs: [https://docs.nexmo.com/verify/api-reference/api-reference#vrequest](https://docs.nexmo.com/verify/api-reference/api-reference#vrequest?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

The response contains a verification request id which you will need to
store temporarily (in the session, database, url etc).

### Check a verification

```python
response = client.check_verification('00e6c3377e5348cdaf567e1417c707a5', code='1234')

if response['status'] == '0':
  print 'Verification complete, event_id=' + response['event_id']
else:
  print 'Error:', response['error_text']
```

Docs: [https://docs.nexmo.com/verify/api-reference/api-reference#check](https://docs.nexmo.com/verify/api-reference/api-reference#check?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

The verification request id comes from the call to the start_verification method.
The PIN code is entered into your application by the user.

### Cancel a verification

```python
client.cancel_verification('00e6c3377e5348cdaf567e1417c707a5')
```

Docs: [https://docs.nexmo.com/verify/api-reference/api-reference#control](https://docs.nexmo.com/verify/api-reference/api-reference#control?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

### Trigger next verification step

```python
client.trigger_next_verification_event('00e6c3377e5348cdaf567e1417c707a5')
```

Docs: [https://docs.nexmo.com/verify/api-reference/api-reference#control](https://docs.nexmo.com/verify/api-reference/api-reference#control?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

## Number Insight API

### Basic Number Insight

```python
client.get_basic_number_insight(number='447700900000')
```

Docs: [https://docs.nexmo.com/number-insight/basic](https://docs.nexmo.com/number-insight/basic?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

### Standard Number Insight

```python
client.get_standard_number_insight(number='447700900000')
```

Docs: [https://docs.nexmo.com/number-insight/standard](https://docs.nexmo.com/number-insight/basic?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

### Advanced Number Insight

```python
client.get_advanced_number_insight(number='447700900000')
```

Docs: [https://docs.nexmo.com/number-insight/advanced](https://docs.nexmo.com/number-insight/advanced?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

## Application API

### Create an application

```python
response = client.create_application(name='Example App', type='voice', answer_url=answer_url, event_url=event_url)
```

Docs: [https://docs.nexmo.com/tools/application-api/api-reference#create](https://docs.nexmo.com/tools/application-api/api-reference#create?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

### Retrieve a list of applications

```python
response = client.get_applications()
```

Docs: [https://docs.nexmo.com/tools/application-api/api-reference#list](https://docs.nexmo.com/tools/application-api/api-reference#list?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

### Retrieve a single application

```python
response = client.get_application(uuid)
```

Docs: [https://docs.nexmo.com/tools/application-api/api-reference#retrieve](https://docs.nexmo.com/tools/application-api/api-reference#retrieve?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

### Update an application

```python
response = client.update_application(uuid, answer_method='POST')
```

Docs: [https://docs.nexmo.com/tools/application-api/api-reference#update](https://docs.nexmo.com/tools/application-api/api-reference#update?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

### Delete an application

```python
response = client.delete_application(uuid)
```

Docs: [https://docs.nexmo.com/tools/application-api/api-reference#delete](https://docs.nexmo.com/tools/application-api/api-reference#delete?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)


## Validate webhook signatures

```python
client = nexmo.Client(signature_secret='secret')

if client.check_signature(request.query):
  # valid signature
else:
  # invalid signature
```

Docs: [https://docs.nexmo.com/messaging/signing-messages](https://docs.nexmo.com/messaging/signing-messages?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

Note: you'll need to contact support@nexmo.com to enable message signing on
your account before you can validate webhook signatures.


## JWT parameters

By default the library generates short lived tokens for JWT authentication.

Use the auth method to specify parameters for a longer life token or to
specify a different token identifier:

```python
client.auth(nbf=nbf, exp=exp, jti=jti)
```


API Coverage
------------

* Account
    * [X] Balance
    * [X] Pricing
    * [X] Settings
    * [X] Top Up
    * [X] Numbers
        * [X] Search
        * [X] Buy
        * [X] Cancel
        * [X] Update
* Number Insight
    * [X] Basic
    * [X] Standard
    * [X] Advanced
    * [ ] Webhook Notification
* Verify
    * [X] Verify
    * [X] Check
    * [X] Search
    * [X] Control
* Messaging 
    * [X] Send
    * [ ] Delivery Receipt
    * [ ] Inbound Messages
    * [X] Search
        * [X] Message
        * [X] Messages
        * [X] Rejections
    * [X] US Short Codes
        * [X] Two-Factor Authentication
        * [X] Event Based Alerts
            * [X] Sending Alerts
            * [X] Campaign Subscription Management
* Voice
    * [X] Outbound Calls
    * [ ] Inbound Call
    * [X] Text-To-Speech Call
    * [X] Text-To-Speech Prompt


Contributing
------------

We :heart: contributions! But if you plan to work on something big or controversial, please [contact us](mailto:devrel@nexmo.com) first!

We recommend working on `nexmo-python` with a [virtualenv][virtualenv]. The following command will install all the Python dependencies you need to run the tests:

```bash
make install
```

The tests are all written with pytest. You run them with:

```bash
make test
```


License
-------

This library is released under the [MIT License][license]

[virtualenv]: https://virtualenv.pypa.io/en/stable/
[report-a-bug]: https://github.com/Nexmo/nexmo-python/issues/new
[pull-request]: https://github.com/Nexmo/nexmo-python/pulls
[signup]: https://dashboard.nexmo.com/sign-up?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library
[license]: LICENSE.txt
