# Vonage Server SDK for Python

<img src="https://developer.nexmo.com/assets/images/Vonage_Nexmo.svg" height="48px" alt="Nexmo is now known as Vonage" />

[![PyPI version](https://badge.fury.io/py/vonage.svg)](https://badge.fury.io/py/vonage)
[![Build Status](https://github.com/Vonage/vonage-python-sdk/workflows/Build/badge.svg)](https://github.com/Vonage/vonage-python-sdk/actions)
[![codecov](https://codecov.io/gh/Vonage/vonage-python-sdk/branch/master/graph/badge.svg)](https://codecov.io/gh/Vonage/vonage-python-sdk)
[![Python versions supported](https://img.shields.io/pypi/pyversions/vonage.svg)](https://pypi.python.org/pypi/vonage)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

This is the Python server SDK for Vonage's API. To use it you'll
need a Vonage account. Sign up [for free at vonage.com][signup].

- [Installation](#installation)
- [Usage](#usage)
- [SMS API](#sms-api)
- [Messages API](#messages-api)
- [Voice API](#voice-api)
- [NCCO Builder](#ncco-builder)
- [Verify V2 API](#verify-v2-api)
- [Verify V1 API](#verify-v1-api)
- [Number Insight API](#number-insight-api)
- [Account API](#account-api)
- [Number Management API](#number-management-api)
- [Pricing API](#pricing-api)
- [Managing Secrets](#managing-secrets)
- [Application API](#application-api)
- [Validating Webhook Signatures](#validate-webhook-signatures)
- [JWT Parameters](#jwt-parameters)
- [Overriding API Attributes](#overriding-api-attributes)
- [Frequently Asked Questions](#frequently-asked-questions)
- [Contributing](#contributing)
- [License](#license)

## Installation

To install the Python client library using pip:

    pip install vonage

To upgrade your installed client library using pip:

    pip install vonage --upgrade

Alternatively, you can clone the repository via the command line:

    git clone git@github.com:Vonage/vonage-python-sdk.git

or by opening it on GitHub desktop.

## Usage

Begin by importing the `vonage` module:

```python
import vonage
```

Then construct a client object with your key and secret:

```python
client = vonage.Client(key=api_key, secret=api_secret)
```

For production, you can specify the `VONAGE_API_KEY` and `VONAGE_API_SECRET`
environment variables instead of specifying the key and secret explicitly.

For newer endpoints that support JWT authentication such as the Voice API,
you can also specify the `application_id` and `private_key` arguments:

```python
client = vonage.Client(application_id=application_id, private_key=private_key)
```

To check signatures for incoming webhook requests, you'll also need
to specify the `signature_secret` argument (or the `VONAGE_SIGNATURE_SECRET`
environment variable).

To use the SDK to call Vonage APIs, pass in dicts with the required options to methods like `Sms.send_message()`. Examples of this are given below.

## Simplified structure for calling API Methods

The client now instantiates a class object for each API when it is created, e.g. `vonage.Client(key="mykey", secret="mysecret")`
instantiates instances of `Account`, `Sms`, `NumberInsight` etc. These instances can now be called directly from `Client`, e.g.

```python
client = vonage.Client(key="mykey", secret="mysecret")

print(f"Account balance is: {client.account.get_balance()}")

print("Sending an SMS")
client.sms.send_message({
    "from": "Vonage",
    "to": "SOME_PHONE_NUMBER",
    "text": "Hello from Vonage's SMS API"
})
```

This means you don't have to create a separate instance of each class to use its API methods. Instead, you can access class methods from the client instance with
```python
client.CLASS_NAME.CLASS_METHOD
```

## SMS API

Although the Messages API adds more messaging channels, the SMS API is still supported.
### Send an SMS

```python
# New way
client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
client.sms.send_message({
    "from": VONAGE_BRAND_NAME,
    "to": TO_NUMBER,
    "text": "A text message sent using the Vonage SMS API",
})

# Old way
from vonage import Sms
sms = Sms(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
sms.send_message({
            "from": VONAGE_BRAND_NAME,
            "to": TO_NUMBER,
            "text": "A text message sent using the Vonage SMS API",
})
```

### Send SMS with unicode

```python
client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_API_SECRET)
client.sms.send_message({
    'from': VONAGE_BRAND_NAME,
    'to': TO_NUMBER,
    'text': 'こんにちは世界',
    'type': 'unicode',
})
```

### Submit SMS Conversion

```python
client = vonage.Client(key=VONAGE_API_KEY, secret=VONAGE_SECRET)
response = client.sms.send_message({
    'from': VONAGE_BRAND_NAME,
    'to': TO_NUMBER,
    'text': 'Hi from Vonage'
})
client.sms.submit_sms_conversion(response['message-id'])
```

### Update the default SMS webhook URLs for callbacks/delivery reciepts
```python
client.sms.update_default_sms_webhook({
    'moCallBackUrl': 'new.url.vonage.com',      # Default inbound sms webhook url
    'drCallBackUrl': 'different.url.vonage.com' # Delivery receipt url
    }})
```

The delivery receipt URL can be unset by sending an empty string.

## Messages API

The Messages API is an API that allows you to send messages via SMS, MMS, WhatsApp, Messenger and Viber. Call the API from your Python code by 
passing a dict of parameters into the `client.messages.send_message()` method.

It accepts JWT or API key/secret authentication.

Some basic samples are below. For more detailed information and code snippets, please visit the [Vonage Developer Documentation](https://developer.vonage.com).

### Send an SMS
```python
responseData = client.messages.send_message({
        'channel': 'sms', 
        'message_type': 'text', 
        'to': '447123456789', 
        'from': 'Vonage',
        'text': 'Hello from Vonage'
    })
```

### Send an MMS
Note: only available in the US. You will need a 10DLC number to send an MMS message.

```python
client.messages.send_message({
        'channel': 'mms', 
        'message_type': 'image', 
        'to': '11112223333', 
        'from': '1223345567',
        'image': {'url': 'https://example.com/image.jpg', 'caption': 'Test Image'}
    })
```

### Send an audio file via WhatsApp

You will need a WhatsApp Business Account to use WhatsApp messaging. WhatsApp restrictions mean that you
must send a template message to a user if they have not previously messaged you, but you can send any message
type to a user if they have messaged your business number in the last 24 hours.

```python
client.messages.send_message({
        'channel': 'whatsapp', 
        'message_type': 'audio', 
        'to': '447123456789', 
        'from': '440123456789',
        'audio': {'url': 'https://example.com/audio.mp3'}
    })
```

### Send a video file via Facebook Messenger

You will need to link your Facebook business page to your Vonage account in the Vonage developer dashboard. (Click on the sidebar
"External Accounts" option to do this.)

```python
client.messages.send_message({
        'channel': 'messenger', 
        'message_type': 'video', 
        'to': '594123123123123', 
        'from': '1012312312312',
        'video': {'url': 'https://example.com/video.mp4'}
    })
```

### Send a text message with Viber

```python
client.messages.send_message({
    'channel': 'viber_service',
    'message_type': 'text',
    'to': '447123456789',
    'from': '440123456789',
    'text': 'Hello from Vonage!'
})
```

## Voice API

### Make a call

```python
client = vonage.Client(application_id=APPLICATION_ID, private_key=PRIVATE_KEY)
client.voice.create_call({
  'to': [{'type': 'phone', 'number': '14843331234'}],
  'from': {'type': 'phone', 'number': '14843335555'},
  'answer_url': ['https://example.com/answer']
})
```

### Retrieve a list of calls

```python
client = vonage.Client(application_id=APPLICATION_ID, private_key=PRIVATE_KEY)
client.voice.get_calls()
```

### Retrieve a single call

```python
client = vonage.Client(application_id=APPLICATION_ID, private_key=PRIVATE_KEY)
client.voice.get_call(uuid)
```

### Update a call

```python
client = vonage.Client(application_id=APPLICATION_ID, private_key=PRIVATE_KEY)
response = client.voice.create_call({
  'to': [{'type': 'phone', 'number': '14843331234'}],
  'from': {'type': 'phone', 'number': '14843335555'},
  'answer_url': ['https://example.com/answer']
})
client.voice.update_call(response['uuid'], action='hangup')
```

### Stream audio to a call

```python
client = vonage.Client(application_id=APPLICATION_ID, private_key=PRIVATE_KEY)
stream_url = 'https://nexmo-community.github.io/ncco-examples/assets/voice_api_audio_streaming.mp3'
response = client.voice.create_call({
  'to': [{'type': 'phone', 'number': '14843331234'}],
  'from': {'type': 'phone', 'number': '14843335555'},
  'answer_url': ['https://example.com/answer']
})
client.voice.send_audio(response['uuid'],stream_url=[stream_url])
```

### Stop streaming audio to a call

```python
client = vonage.Client(application_id='0d4884d1-eae8-4f18-a46a-6fb14d5fdaa6', private_key='./private.key')
stream_url = 'https://nexmo-community.github.io/ncco-examples/assets/voice_api_audio_streaming.mp3'
response = client.voice.create_call({
  'to': [{'type': 'phone', 'number': '14843331234'}],
  'from': {'type': 'phone', 'number': '14843335555'},
  'answer_url': ['https://example.com/answer']
})
client.voice.send_audio(response['uuid'],stream_url=[stream_url])
client.voice.stop_audio(response['uuid'])
```

### Send a synthesized speech message to a call

```python
client = vonage.Client(application_id=APPLICATION_ID, private_key=PRIVATE_KEY)
response = client.voice.create_call({
  'to': [{'type': 'phone', 'number': '14843331234'}],
  'from': {'type': 'phone', 'number': '14843335555'},
  'answer_url': ['https://example.com/answer']
})
client.voice.send_speech(response['uuid'], text='Hello from vonage')
```

### Stop sending a synthesized speech message to a call

```python
client = vonage.Client(application_id=APPLICATION_ID, private_key=APPLICATION_ID)
response = client.voice.create_call({
  'to': [{'type': 'phone', 'number': '14843331234'}],
  'from': {'type': 'phone', 'number': '14843335555'},
  'answer_url': ['https://example.com/answer']
})
client.voice.send_speech(response['uuid'], text='Hello from vonage')
client.voice.stop_speech(response['uuid'])
```

### Send DTMF tones to a call

```python
client = vonage.Client(application_id=APPLICATION_ID, private_key=PRIVATE_KEY)
response = client.voice.create_call({
  'to': [{'type': 'phone', 'number': '14843331234'}],
  'from': {'type': 'phone', 'number': '14843335555'},
  'answer_url': ['https://example.com/answer']
})
client.voice.send_dtmf(response['uuid'], digits='1234')
```

### Get recording

```python
response = client.get_recording(RECORDING_URL)
```

## NCCO Builder

The SDK contains a builder to help you create Call Control Objects (NCCOs) for use with the Vonage Voice API.

For more information, [check the full NCCO reference documentation on the Vonage website](https://developer.vonage.com/voice/voice-api/ncco-reference).

An NCCO is a list of "Actions": steps to be followed when a call is initiated or received.

Use the builder to construct valid NCCO actions, which are modelled in the SDK as [Pydantic](https://docs.pydantic.dev) models, and build them into an NCCO. The NCCO actions supported by the builder are:

* Record
* Conversation
* Connect
* Talk
* Stream
* Input
* Notify

### Construct actions

```python
record = Ncco.Record(eventUrl=['https://example.com'])
talk = Ncco.Talk(text='Hello from Vonage!', bargeIn=True, loop=5, premium=True)
```

The Connect action has each valid endpoint type (phone, application, WebSocket, SIP and VBC) specified as a Pydantic model so these can be validated, though it is also possible to pass in a dict with the endpoint properties directly into the `Ncco.Connect` object.

This example shows a Connect action created with an endpoint object.

```python
phone = ConnectEndpoints.PhoneEndpoint(
        number='447000000000',
        dtmfAnswer='1p2p3p#**903#',
    )
connect = Ncco.Connect(endpoint=phone, eventUrl=['https://example.com/events'], from_='447000000000')
```

This example shows a different Connect action, created with a dictionary.

```python
connect = Ncco.Connect(endpoint={'type': 'phone', 'number': '447000000000', 'dtmfAnswer': '2p02p'}, randomFromNumber=True)
```

### Build into an NCCO

Create an NCCO from the actions with the `Ncco.build_ncco` method. This will be returned as a list of dicts representing each action and can be used in calls to the Voice API.

```python
ncco = Ncco.build_ncco(record, connect, talk)

response = client.voice.create_call({
    'to': [{'type': 'phone', 'number': TO_NUMBER}],
    'from': {'type': 'phone', 'number': VONAGE_NUMBER},
    'ncco': ncco
})

pprint(response)
```

### Note on from_ parameter in connect action

When using the `connect` action, use the parameter `from_` to specify the recipient (as `from` is a reserved keyword in Python!)

## Verify V2 API

V2 of the Vonage Verify API lets you send verification codes via SMS, WhatsApp, Voice and Email

You can also verify a user by WhatsApp Interactive Message or by Silent Authentication on their mobile device.

### Send a verification code

```python
params = {
    'brand': 'ACME, Inc', 
    'workflow': [{'channel': 'sms', 'to': '447700900000'}]
}
verify_request = verify2.new_request(params)
```

### Use silent authentication, with email as a fallback

```python
params = {
    'brand': 'ACME, Inc', 
    'workflow': [
        {'channel': 'silent_auth', 'to': '447700900000'},
        {'channel': 'email', 'to': 'customer@example.com', 'from': 'business@example.com'}
    ]
}
verify_request = verify2.new_request(params)
```

### Send a verification code with custom options, including a custom code

```python
params = {
    'locale': 'en-gb',
    'channel_timeout': 120,
    'client_ref': 'my client reference',
    'code': 'asdf1234',
    'brand': 'ACME, Inc',
    'workflow': [{'channel': 'sms', 'to': '447700900000', 'app_hash': 'asdfghjklqw'}],
}
verify_request = verify2.new_request(params)
```

### Send a verification request to a blocked network

This feature is only enabled if you have requested for it to be added to your account.

```python
params = {
    'brand': 'ACME, Inc', 
    'fraud_check': False, 
    'workflow': [{'channel': 'sms', 'to': '447700900000'}]
}
verify_request = verify2.new_request(params)
```

### Check a verification code

```python
verify2.check_code(REQUEST_ID, CODE)
```

### Cancel an ongoing verification

```python
verify2.cancel_verification(REQUEST_ID)
```

## Verify V1 API

### Search for a Verification request

```python
client = vonage.Client(key='API_KEY', secret='API_SECRET')

response = client.verify.search('69e2626cbc23451fbbc02f627a959677')

if response is not None:
    print(response['status'])
```

### Send verification code

```python
client = vonage.Client(key='API_KEY', secret='API_SECRET')

response = client.verify.start_verification(number=RECIPIENT_NUMBER, brand='AcmeInc')

if response["status"] == "0":
    print("Started verification request_id is %s" % (response["request_id"]))
else:
    print("Error: %s" % response["error_text"])
```

### Send verification code with workflow

```python
client = vonage.Client(key='API_KEY', secret='API_SECRET')

response = client.verify.start_verification(number=RECIPIENT_NUMBER, brand='AcmeInc', workflow_id=1)

if response["status"] == "0":
    print("Started verification request_id is %s" % (response["request_id"]))
else:
    print("Error: %s" % response["error_text"])
```

### Check verification code

```python
client = vonage.Client(key='API_KEY', secret='API_SECRET')

response = client.verify.check(REQUEST_ID, code=CODE)

if response["status"] == "0":
    print("Verification successful, event_id is %s" % (response["event_id"]))
else:
    print("Error: %s" % response["error_text"])
```

### Cancel Verification Request

```python
client = vonage.Client(key='API_KEY', secret='API_SECRET')

response = client.verify.cancel(REQUEST_ID)

if response["status"] == "0":
    print("Cancellation successful")
else:
    print("Error: %s" % response["error_text"])
```

### Trigger next verification proccess

```python
client = vonage.Client(key='API_KEY', secret='API_SECRET')

response = client.verify.trigger_next_event(REQUEST_ID)

if response["status"] == "0":
    print("Next verification stage triggered")
else:
    print("Error: %s" % response["error_text"])
```

### Send payment authentication code

```python
client = vonage.Client(key='API_KEY', secret='API_SECRET')

response = client.verify.psd2(number=RECIPIENT_NUMBER, payee=PAYEE, amount=AMOUNT)

if response["status"] == "0":
    print("Started PSD2 verification request_id is %s" % (response["request_id"]))
else:
    print("Error: %s" % response["error_text"])
```

### Send payment authentication code with workflow

```python
client = vonage.Client(key='API_KEY', secret='API_SECRET')

client.verify.psd2(number=RECIPIENT_NUMBER, payee=PAYEE, amount=AMOUNT, workflow_id: WORKFLOW_ID)

if response["status"] == "0":
    print("Started PSD2 verification request_id is %s" % (response["request_id"]))
else:
    print("Error: %s" % response["error_text"])
```

## Number Insight API

### Basic Number Insight

```python
client.number_insight.get_basic_number_insight(number='447700900000')
```

Docs: [https://developer.nexmo.com/api/number-insight#getNumberInsightBasic](https://developer.nexmo.com/api/number-insight?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#getNumberInsightBasic)

### Standard Number Insight

```python
client.number_insight.get_standard_number_insight(number='447700900000')
```

Docs: [https://developer.nexmo.com/api/number-insight#getNumberInsightStandard](https://developer.nexmo.com/api/number-insight?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#getNumberInsightStandard)

### Advanced Number Insight

```python
client.number_insight.get_advanced_number_insight(number='447700900000')
```

Docs: [https://developer.nexmo.com/api/number-insight#getNumberInsightAdvanced](https://developer.nexmo.com/api/number-insight?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#getNumberInsightAdvanced)

## Account API

### Get your account balance
```python
client.account.get_balance()
```

### Top up your account
This feature is only enabled when you enable auto-reload for your account in the dashboard.
```python
# trx is the reference from when auto-reload was enabled and money was added
client.account.topup(trx=transaction_reference) 
```

## Pricing API

### Get pricing for a single country
```python
client.account.get_country_pricing(country_code='GB', type='sms') # Default type is sms
```

### Get pricing for all countries
```python
client.account.get_all_countries_pricing(type='sms') # Default type is sms, can be voice
```

### Get pricing for a specific dialling prefix
```python
client.account.get_prefix_pricing(prefix='44', type='sms')
```

## Managing Secrets

An API is provided to allow you to rotate your API secrets. You can create a new secret (up to a maximum of two secrets) and delete the existing one once all applications have been updated.

### List Secrets

```python
secrets = client.account.list_secrets(API_KEY)
```

### Get information about a specific secret

```python
secrets = client.account.get_secret(API_KEY, secret_id)
```

### Create A New Secret

Create a new secret (the created dates will help you know which is which):

```python
client.account.create_secret(API_KEY, 'awes0meNewSekret!!;');
```

### Delete A Secret

Delete the old secret (any application still using these credentials will stop working):

```python
client.account.revoke_secret(API_KEY, 'my-secret-id')
```

## Application API

### Create an application

```python
response = client.application.create_application({name='Example App', type='voice'})
```

Docs: [https://developer.nexmo.com/api/application.v2#createApplication](https://developer.nexmo.com/api/application.v2#createApplication?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#create-an-application)

### Retrieve a list of applications

```python
response = client.application.list_applications()
```

Docs: [https://developer.nexmo.com/api/application.v2#listApplication](https://developer.nexmo.com/api/application.v2#listApplication?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#retrieve-your-applications)

### Retrieve a single application

```python
response = client.application.get_application(uuid)
```

Docs: [https://developer.nexmo.com/api/application.v2#getApplication](https://developer.nexmo.com/api/application.v2#getApplication?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#retrieve-an-application)

### Update an application

```python
response = client.application.update_application(uuid, answer_method='POST')
```

Docs: [https://developer.nexmo.com/api/application.v2#updateApplication](https://developer.nexmo.com/api/application.v2#updateApplication?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#update-an-application)

### Delete an application

```python
response = client.application.delete_application(uuid)
```

Docs: [https://developer.nexmo.com/api/application.v2#deleteApplication](https://developer.nexmo.com/api/application.v2#deleteApplication?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#destroy-an-application)

## Validate webhook signatures

```python
client = vonage.Client(signature_secret='secret')

if client.check_signature(request.query):
  # valid signature
else:
  # invalid signature
```

Docs: [https://developer.nexmo.com/concepts/guides/signing-messages](https://developer.nexmo.com/concepts/guides/signing-messages?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library)

Note: you'll need to contact support@nexmo.com to enable message signing on
your account before you can validate webhook signatures.

## JWT parameters

By default, the library generates short-lived tokens for JWT authentication.

Use the auth method to specify parameters for a longer life token or to
specify a different token identifier:

```python
client.auth(nbf=nbf, exp=exp, jti=jti)
```

## Overriding API Attributes

In order to rewrite/get the value of variables used across all the Vonage classes Python uses `Call by Object Reference` that allows you to create a single client for Sms/Voice Classes. This means that if you make a change on a client instance this will be available for the Sms class.

An example using setters/getters with `Object references`:

```python
from vonage import Client, Sms

#Defines the client
client = Client(key='YOUR_API_KEY', secret='YOUR_API_SECRET')
print(client.host()) # using getter for host -- value returned: rest.nexmo.com

#Define the sms instance
sms = Sms(client)

#Change the value in client
client.host('mio.nexmo.com') #Change host to mio.nexmo.com - this change will be available for sms

```

### Overriding API Host / Host Attributes

These attributes are private in the client class and the only way to access them is using the getters/setters we provide.

```python
from vonage import Client

client = Client(key='YOUR_API_KEY', secret='YOUR_API_SECRET')
print(client.host()) # return rest.nexmo.com
client.host('mio.nexmo.com') # rewrites the host value to mio.nexmo.com
print(client.api_host()) # returns api.vonage.com
client.api_host('myapi.vonage.com') # rewrite the value of api_host
```

## Frequently Asked Questions

### Supported APIs

The following is a list of Vonage APIs and whether the Python SDK provides support for them:

| API                   |  API Release Status  | Supported? |
| --------------------- | :------------------: | :--------: |
| Account API           | General Availability |     ✅     |
| Alerts API            | General Availability |     ✅     |
| Application API       | General Availability |     ✅     |
| Audit API             |         Beta         |     ❌     |
| Conversation API      |         Beta         |     ❌     |
| Dispatch API          |         Beta         |     ❌     |
| External Accounts API |         Beta         |     ❌     |
| Media API             |         Beta         |     ❌     |
| Messages API          | General Availability |     ✅     |
| Number Insight API    | General Availability |     ✅     |
| Number Management API | General Availability |     ✅     |
| Pricing API           | General Availability |     ✅     |
| Redact API            |   Developer Preview  |     ❌     |
| Reports API           |         Beta         |     ❌     |
| SMS API               | General Availability |     ✅     |
| Verify API            | General Availability |     ✅     |
| Voice API             | General Availability |     ✅     |

### asyncio Support

[asyncio](https://docs.python.org/3/library/asyncio.html) is a library to write **concurrent** code using the **async/await** syntax.

We don't currently support asyncio in the Python SDK but we are planning to do so in upcoming releases.

## Contributing

We :heart: contributions! But if you plan to work on something big or controversial, please [contact us](mailto:devrel@vonage.com) first!

We recommend working on `vonage-python-sdk` with a [virtualenv][virtualenv]. The following command will install all the Python dependencies you need to run the tests:

```bash
make install
```

The tests are all written with pytest. You run them with:

```bash
make test
```

## License

This library is released under the [Apache License][license].

[virtualenv]: https://virtualenv.pypa.io/en/stable/
[report-a-bug]: https://github.com/Vonage/vonage-python-sdk/issues/new
[pull-request]: https://github.com/Vonage/vonage-python-sdk/pulls
[signup]: https://dashboard.nexmo.com/sign-up?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library
[license]: LICENSE.txt
