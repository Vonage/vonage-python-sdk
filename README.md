Nexmo Client Library for Python
===============================

[![PyPI version](https://badge.fury.io/py/nexmo.svg)](https://badge.fury.io/py/nexmo) [![Build Status](https://api.travis-ci.org/Nexmo/nexmo-python.svg?branch=master)](https://travis-ci.org/Nexmo/nexmo-python)

This is the Python client library for Nexmo's API. To use it you'll
need a Nexmo account. Sign up [for free at nexmo.com][signup].

* [Installation](#installation)
* [Usage](#usage)
* [Examples](#examples)
* [License](#license)


Installation
------------

To install the Python client library using pip:

    pip install nexmo

Alternatively you can clone the repository:

    git clone git@github.com:Nexmo/nexmo-python.git


Usage
-----

Specify your credentials using the `NEXMO_API_KEY` and `NEXMO_API_SECRET`
environment variables; import the nexmo package; and construct a client object.
For example:

```python
import nexmo

client = nexmo.Client()
```

Alternatively you can specify your credentials directly using the `key`
and `secret` keyword args:

```python
import nexmo

client = nexmo.Client(key='YOUR-API-KEY', secret='YOUR-API-SECRET')
```


Examples
--------

### Sending a message

To use [Nexmo's SMS API][doc_sms] to send an SMS message, call the send_message
method with a dictionary containing the API parameters. For example:

```python
response = client.send_message({'from': 'Python', 'to': 'YOUR-NUMBER', 'text': 'Hello world'})

response = response['messages'][0]

if response['status'] == '0':
  print 'Sent message', response['message-id']

  print 'Remaining balance is', response['remaining-balance']
else:
  print 'Error:', response['error-text']
```

### Fetching a message

You can retrieve a message log from the API using the ID of the message:

```python
message = client.get_message('02000000DA7C52E7')

print 'The body of the message was:', message['body']
```

### Starting a verification

Nexmo's [Verify API][doc_verify] makes it easy to prove that a user has provided their
own phone number during signup, or implement second factor authentication during signin.

You can start the verification process by calling the send_verification_request method:

```python
response = client.send_verification_request(number='441632960960', brand='MyApp')

if response['status'] == '0':
  print 'Started verification', response['request_id']
else:
  print 'Error:', response['error_text']
```

### Controlling a verification

To cancel an in-progress verification or to trigger the next attempt to
send the confirmation code, call the control_verification_request method:

```python
client.control_verification_request(cmd='cancel', request_id='00e6c3377e5348cdaf567e1417c707a5')

client.control_verification_request(cmd='trigger_next_event', request_id='00e6c3377e5348cdaf567e1417c707a5')
```

### Checking a verification

To check a verification, call the check_verification_request method with
the PIN code provided by the user and the id of the verification request:

```python
response = client.check_verification_request(code='1234', request_id='00e6c3377e5348cdaf567e1417c707a5')

if response['status'] == '0':
  print 'Verification complete, event ', response['event_id']
else:
  print 'Error:', response['error_text']
```

### Start an outbound call

Use Nexmo's [Call API][doc_call] to initiate an outbound voice call by calling
the initiate_call method with the number to call and the URL to a VoiceXML
resource for controlling the call:

```python
response = client.initiate_call(to='447525856424', answer_url='http://example.com/call.xml')

if response['status'] == '0':
  print 'Started call', response['call-id']
else:
  print 'Error:', response['error-text']
```


License
-------

This library is released under the [MIT License][license]

[signup]: https://dashboard.nexmo.com/sign-up?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library
[doc_sms]: https://docs.nexmo.com/messaging/sms-api?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library
[doc_verify]: https://docs.nexmo.com/verify/api-reference?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library
[doc_call]: https://docs.nexmo.com/voice/call?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library
[license]: LICENSE.txt
