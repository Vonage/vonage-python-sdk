# Nexmo Client Library for Python

[![PyPI version](https://badge.fury.io/py/nexmo.svg)](https://badge.fury.io/py/nexmo)
[![Build Status](https://api.travis-ci.org/Nexmo/nexmo-python.svg?branch=master)](https://travis-ci.org/Nexmo/nexmo-python)
[![Coverage Status](https://coveralls.io/repos/github/Nexmo/nexmo-python/badge.svg?branch=master)](https://coveralls.io/github/Nexmo/nexmo-python?branch=master)
[![Python versions supported](https://img.shields.io/pypi/pyversions/nexmo.svg)](https://pypi.python.org/pypi/nexmo)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)

This is the Python client library for Nexmo's API. To use it you'll
need a Nexmo account. Sign up [for free at nexmo.com][signup].


* [Installation](#installation)
* [Usage](#usage)
* [SMS API](#sms-api)
* [Voice API](#voice-api)
* [Verify API](#verify-api)
* [Number Insight API](#number-insight-api)
* [Number Management API](#number-management-api)
* [Managing Secrets](#managing-secrets)
* [Application API](#application-api)
* [Overriding API Attributes](#overriding-api-attributes)
* [License](#license)


## Installation

To install the Python client library using pip:

    pip install nexmo

To upgrade your installed client library using pip:

    pip install nexmo --upgrade

Alternatively, you can clone the repository via the command line:

    git clone git@github.com:Nexmo/nexmo-python.git

or by opening it on GitHub desktop.

## Usage

Begin by importing the `nexmo` module:

```python
import nexmo
```

Then construct a client object with your key and secret:

```python
client = nexmo.Client(key=api_key, secret=api_secret)
```

For production, you can specify the `NEXMO_API_KEY` and `NEXMO_API_SECRET`
environment variables instead of specifying the key and secret explicitly.

For newer endpoints that support JWT authentication such as the Voice API,
you can also specify the `application_id` and `private_key` arguments:

```python
client = nexmo.Client(application_id=application_id, private_key=private_key)
```

To check signatures for incoming webhook requests, you'll also need
to specify the `signature_secret` argument (or the `NEXMO_SIGNATURE_SECRET`
environment variable).

## SMS API

## SMS Class

### Creating an instance of the SMS class

To create an instance of the SMS class follow these steps:

- Import the class

```python
#Option 1
from nexmo import Sms

#Option 2
from nexmo.sms import Sms

#Option 3
import nexmo #then tou can use nexmo.Sms() to create an instance
```

- Create an instance

```python
#Option 1 - pass key and secret to the constructor
sms = Sms(key=NEXMO_API_KEY, secret=NEXMO_API_SECRET)

#Option 2 - Create a client instance and then pass the client to the Sms instance
client = Client(key=NEXMO_API_KEY, secret=NEXMO_API_SECRET)
sms = Sms(client)
```

### Send an SMS

```python
    responseData = client.send_message(
        {
            "from": NEXMO_BRAND_NAME,
            "to": TO_NUMBER,
            "text": "A text message sent using the Nexmo SMS API",
        }
    )
```

Reference: [Send sms](https://developer.nexmo.com/messaging/sms/code-snippets/send-an-sms)

**Using the Sms class**

```python
from nexmo import Sms
sms = Sms(key=NEXMO_API_KEY, secret=NEXMO_API_SECRET)
sms.send_message({
            "from": NEXMO_BRAND_NAME,
            "to": TO_NUMBER,
            "text": "A text message sent using the Nexmo SMS API",
})
```

Support link: [Send sms](https://gitlab.com/codeonrocks/client/nexmo-python/uploads/17e17c6f05f6d28c53596f2412c627c2/SMSSendMessage.PNG)

### Send SMS with unicode

```python
responseData = client.send_message({
    'from': NEXMO_BRAND_NAME,
    'to': TO_NUMBER,
    'text': 'こんにちは世界',
    'type': 'unicode',
})
```

Reference: [Send sms with unicode](https://developer.nexmo.com/messaging/sms/code-snippets/send-an-sms-with-unicode)

**Using Sms Class**

```python
sms.send_message({
    'from': NEXMO_BRAND_NAME,
    'to': TO_NUMBER,
    'text': 'こんにちは世界',
    'type': 'unicode',
})
```

### Submit SMS Conversion

```python
client.submit_sms_conversion("a-message-id")
```

**With the SMS Class**

```python
from nexmo import Client, Sms
client = Client(key=NEXMO_API_KEY, secret=NEXMO_SECRET)
sms = Sms(client)
response = sms.send_message({
    'from': NEXMO_BRAND_NAME,
    'to': TO_NUMBER,
    'text': 'Hi from Vonage'
})
sms.submit_sms_conversion(response['message-id'])
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

Docs: [https://developer.nexmo.com/api/voice#createCall](https://developer.nexmo.com/api/voice?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#createCall)

**with voice class**

```python
from nexmo import Client, Voice
client = Client(application_id=APPLICATION_ID, private_key=PRIVATE_KEY)
voice = Voice(client)
voice.create_all({
  'to': [{'type': 'phone', 'number': '14843331234'}],
  'from': {'type': 'phone', 'number': '14843335555'},
  'answer_url': ['https://example.com/answer']
})
```

Testing screenshots:[create call](https://gitlab.com/codeonrocks/client/nexmo-python/uploads/fc104415f55a4ad22ecf8defd90b926b/NexmoVoiceUsage.PNG)

### Retrieve a list of calls

```python
response = client.get_calls()
```

Docs: [https://developer.nexmo.com/api/voice#getCalls](https://developer.nexmo.com/api/voice?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#getCalls)

**with voice class**

```python
from nexmo import Client, Voice
client = Client(application_id=APPLICATION_ID, private_key=PRIVATE_KEY)
voice = Voice(client)
voice.get_calls()
```

Testing screenshots: [get calls](https://gitlab.com/codeonrocks/client/nexmo-python/uploads/a5cc162f255dc83b8cdd1d2f80531925/NexmoVoiceGetCalls.PNG)

### Retrieve a single call

```python
response = client.get_call(uuid)
```

Docs: [https://developer.nexmo.com/api/voice#getCall](https://developer.nexmo.com/api/voice?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#getCall)

**with voice class**

```python
from nexmo import Client, Voice
client = Client(application_id=APPLICATION_ID, private_key=PRIVATE_KEY)
voice = Voice(client)
voice.get_call(uuid)
```

Testing Screenshots: [get single call](https://gitlab.com/codeonrocks/client/nexmo-python/uploads/5cef34880afdc6a4c3cd3dee0e84aae2/NexmoVoiceGetSingleCall.PNG)

### Update a call

```python
response = client.update_call(uuid, action='hangup')
```

Docs: [https://developer.nexmo.com/api/voice#updateCall](https://developer.nexmo.com/api/voice?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#updateCall)

**with voice class**

```python
from nexmo import Client, Voice
client = Client(application_id=APPLICATION_ID, private_key=PRIVATE_KEY)
voice = Voice(client)
response = voice.create_all({
  'to': [{'type': 'phone', 'number': '14843331234'}],
  'from': {'type': 'phone', 'number': '14843335555'},
  'answer_url': ['https://example.com/answer']
})
voice.update_call(response['uuid'], action='hangup')
```

Support Link: [update call](https://gitlab.com/codeonrocks/client/nexmo-python/uploads/bdf7c0990b6d4019a2758a7148fdf1e4/VoiceUpdateCall.PNG)

### Stream audio to a call

```python
stream_url = 'https://nexmo-community.github.io/ncco-examples/assets/voice_api_audio_streaming.mp3'

response = client.send_audio(uuid, stream_url=[stream_url])
```

Docs: [https://developer.nexmo.com/api/voice#startStream](https://developer.nexmo.com/api/voice?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#startStream)

**with voice class**

```python
from nexmo import Client, Voice
client = Client(application_id=APPLICATION_ID, private_key=PRIVATE_KEY)
voice = Voice(client)
stream_url = 'https://nexmo-community.github.io/ncco-examples/assets/voice_api_audio_streaming.mp3'
response = voice.create_call({
  'to': [{'type': 'phone', 'number': '14843331234'}],
  'from': {'type': 'phone', 'number': '14843335555'},
  'answer_url': ['https://example.com/answer']
})
voice.send_audio(response['uuid'],stream_url=[stream_url])
```

Support link: [Send audio stream](https://gitlab.com/codeonrocks/client/nexmo-python/uploads/fdc22d76f6bb5c8abf625311f222512a/VoiceSendAudioStream.PNG)

### Stop streaming audio to a call

```python
response = client.stop_audio(uuid)
```

Docs: [https://developer.nexmo.com/api/voice#stopStream](https://developer.nexmo.com/api/voice?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#stopStream)

**Using voice class**

```python
from nexmo import Client, Voice
client = Client(application_id='0d4884d1-eae8-4f18-a46a-6fb14d5fdaa6', private_key='./private.key')
voice = Voice(client)
stream_url = 'https://nexmo-community.github.io/ncco-examples/assets/voice_api_audio_streaming.mp3'
response = voice.create_call({
  'to': [{'type': 'phone', 'number': '14843331234'}],
  'from': {'type': 'phone', 'number': '14843335555'},
  'answer_url': ['https://example.com/answer']
})
voice.send_audio(response['uuid'],stream_url=[stream_url])
voice.stop_audio(response['uuid'])
```

Support Link: [Stop audio stream](https://gitlab.com/codeonrocks/client/nexmo-python/uploads/589be23c5a31694e310aacf0fa6a2314/VoiceSendStopAudioStream.PNG)

### Send a synthesized speech message to a call

```python
response = client.send_speech(uuid, text='Hello')
```

Docs: [https://developer.nexmo.com/api/voice#startTalk](https://developer.nexmo.com/api/voice?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#startTalk)

**Using voice class**

```python
from nexmo import Client, Voice
client = Client(application_id=APPLICATION_ID, private_key=PRIVATE_KEY)
voice = Voice(client)
response = voice.create_call({
  'to': [{'type': 'phone', 'number': '14843331234'}],
  'from': {'type': 'phone', 'number': '14843335555'},
  'answer_url': ['https://example.com/answer']
})
voice.send_speech(response['uuid'], text='Hello from nexmo')
```

Support link: [Send speech](https://gitlab.com/codeonrocks/client/nexmo-python/uploads/d608bfe3b1fb288c9f4854d76fba37af/VoiceSendSpeech.PNG)

### Stop sending a synthesized speech message to a call

```python
response = client.stop_speech(uuid)
```

Docs: [https://developer.nexmo.com/api/voice#stopTalk](https://developer.nexmo.com/api/voice?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#stopTalk)

**Using voice class**

```python
>>> from nexmo import Client, Voice
>>> client = Client(application_id=APPLICATION_ID, private_key=APPLICATION_ID)
>>> voice = Voice(client)
>>> response = voice.create_call({
  'to': [{'type': 'phone', 'number': '14843331234'}],
  'from': {'type': 'phone', 'number': '14843335555'},
  'answer_url': ['https://example.com/answer']
})
>>> voice.send_speech(response['uuid'], text='Hello from nexmo')
>>> voice.stop_speech(response['uuid'])
```

Support link: [Stop speech](https://gitlab.com/codeonrocks/client/nexmo-python/uploads/246801f2e34d147955ac3531e4e7b65d/VoiceSendStopSpeech.PNG)

### Send DTMF tones to a call

```python
response = client.send_dtmf(uuid, digits='1234')
```

Docs: [https://developer.nexmo.com/api/voice#startDTMF](https://developer.nexmo.com/api/voice?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#startDTMF)

**Using voice class**

```python
from nexmo import Client, Voice
client = Client(application_id=APPLICATION_ID, private_key=PRIVATE_KEY)
voice = Voice(client)
response = voice.create_call({
  'to': [{'type': 'phone', 'number': '14843331234'}],
  'from': {'type': 'phone', 'number': '14843335555'},
  'answer_url': ['https://example.com/answer']
})
voice.send_dtmf(response['uuid'], digits='1234')
```

Support link: [Send DTMF](https://gitlab.com/codeonrocks/client/nexmo-python/uploads/7c4b25014d6c94eb886cbaa9a55d2ae3/VoiceSendDTMF.PNG)

### Get recording

```python
response = client.get_recording(RECORDING_URL)
```

## Verify API

### Start a verification

```python
response = client.start_verification(number='441632960960', brand='MyApp')

if response['status'] == '0':
  print('Started verification request_id={request_id}'.format(request_id=response['request_id']))
else:
  print('Error:', response['error_text'])
```

Docs: [https://developer.nexmo.com/api/verify#verify-request](https://developer.nexmo.com/api/verify?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#verify-request)

The response contains a verification request id which you will need to
store temporarily (in the session, database, url, etc).

### Check a verification

```python
response = client.check_verification('00e6c3377e5348cdaf567e1417c707a5', code='1234')

if response['status'] == '0':
  print('Verification complete, event_id={event_id}'.format(event_id=response['event_id']))
else:
  print('Error:', response['error_text'])
```

Docs: [https://developer.nexmo.com/api/verify#verify-check](https://developer.nexmo.com/api/verify?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#verify-check)

The verification request id comes from the call to the start_verification method.
The PIN code is entered into your application by the user.

### Cancel a verification

```python
client.cancel_verification('00e6c3377e5348cdaf567e1417c707a5')
```

Docs: [https://developer.nexmo.com/api/verify#verify-control](https://developer.nexmo.com/api/verify?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#verify-control)

### Trigger next verification step

```python
client.trigger_next_verification_event('00e6c3377e5348cdaf567e1417c707a5')
```

Docs: [https://developer.nexmo.com/api/verify#verify-control](https://developer.nexmo.com/api/verify?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#verify-control)

## Number Insight API

### Basic Number Insight

```python
client.get_basic_number_insight(number='447700900000')
```

Docs: [https://developer.nexmo.com/api/number-insight#getNumberInsightBasic](https://developer.nexmo.com/api/number-insight?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#getNumberInsightBasic)

### Standard Number Insight

```python
client.get_standard_number_insight(number='447700900000')
```

Docs: [https://developer.nexmo.com/api/number-insight#getNumberInsightStandard](https://developer.nexmo.com/api/number-insight?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#getNumberInsightStandard)

### Advanced Number Insight

```python
client.get_advanced_number_insight(number='447700900000')
```

Docs: [https://developer.nexmo.com/api/number-insight#getNumberInsightAdvanced](https://developer.nexmo.com/api/number-insight?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#getNumberInsightAdvanced)

## Managing Secrets

An API is provided to allow you to rotate your API secrets. You can create a new secret (up to a maximum of two secrets) and delete the existing one once all applications have been updated.

### List Secrets

```python
secrets = client.list_secrets(API_KEY)
```

### Create A New Secret

Create a new secret (the created dates will help you know which is which):

```python
client.create_secret(API_KEY, 'awes0meNewSekret!!;');
```

### Delete A Secret

Delete the old secret (any application still using these credentials will stop working):

```python
client.delete_secret(API_KEY, 'my-secret-id')
```

## Application API

### Create an application

```python
response = client.application_v2.create_application({name='Example App', type='voice'})
```

Docs: [https://developer.nexmo.com/api/application.v2#createApplication](https://developer.nexmo.com/api/application.v2#createApplication?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#create-an-application)

### Retrieve a list of applications

```python
response = client.application_v2.list_applications()
```

Docs: [https://developer.nexmo.com/api/application.v2#listApplication](https://developer.nexmo.com/api/application.v2#listApplication?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#retrieve-your-applications)

### Retrieve a single application

```python
response = client.application_v2.get_application(uuid)
```

Docs: [https://developer.nexmo.com/api/application.v2#getApplication](https://developer.nexmo.com/api/application.v2#getApplication?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#retrieve-an-application)

### Update an application

```python
response = client.application_v2.update_application(uuid, answer_method='POST')
```

Docs: [https://developer.nexmo.com/api/application.v2#updateApplication](https://developer.nexmo.com/api/application.v2#updateApplication?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#update-an-application)

### Delete an application

```python
response = client.application_v2.delete_application(uuid)
```

Docs: [https://developer.nexmo.com/api/application.v2#deleteApplication](https://developer.nexmo.com/api/application.v2#deleteApplication?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library#destroy-an-application)

## Validate webhook signatures

```python
client = nexmo.Client(signature_secret='secret')

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

In order to rewrite/get the value of variables used across all the Nexmo classes Python uses `Call by Object Reference` that allows you to create a single client for Sms/Voice Classes. This means that if you make a change on a client instance this will be available for the Sms class.

An example using setters/getters with `Object references`:

```python
from nexmo import Client, Sms

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
from nexmo import Client

client = Client(key='YOUR_API_KEY', secret='YOUR_API_SECRET')
print(client.host()) # return rest.nexmo.com
client.host('mio.nexmo.com') # rewrites the host value to mio.nexmo.com
print(client.api_host()) # returns api.nexmo.com
client.api_host('myapi.nexmo.com') # rewrite the value of api_host
```

## Contributing

We :heart: contributions! But if you plan to work on something big or controversial, please [contact us](mailto:devrel@nexmo.com) first!

We recommend working on `nexmo-python` with a [virtualenv][virtualenv]. The following command will install all the Python dependencies you need to run the tests:

```bash
make install
```

The tests are all written with pytest. You run them with:

```bash
make test
```

## License

This library is released under the [MIT License][license].

[virtualenv]: https://virtualenv.pypa.io/en/stable/
[report-a-bug]: https://github.com/Nexmo/nexmo-python/issues/new
[pull-request]: https://github.com/Nexmo/nexmo-python/pulls
[signup]: https://dashboard.nexmo.com/sign-up?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library
[license]: LICENSE.txt
