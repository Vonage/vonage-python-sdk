Nexmo Client Library for Python
===============================

[![PyPI version](https://badge.fury.io/py/nexmo.svg)](https://badge.fury.io/py/nexmo) [![Build Status](https://api.travis-ci.org/Nexmo/nexmo-python.svg?branch=master)](https://travis-ci.org/Nexmo/nexmo-python)

This is the Python client library for Nexmo's API. To use it you'll
need a Nexmo account. Sign up [for free at nexmo.com][signup].

* [Installation](#installation)
* [Usage](#usage)
* [Examples](#examples)
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

You can start the verification process by calling the start_verification method:

```python
response = client.start_verification(number='441632960960', brand='MyApp')

if response['status'] == '0':
  print 'Started verification request_id=' + response['request_id']
else:
  print 'Error:', response['error_text']
```

The response contains a verification request id which you will need to
store temporarily (in the session, database, url etc).

### Controlling a verification

Call the cancel_verification method with the verification request id
to cancel an in-progress verification:

```python
client.cancel_verification('00e6c3377e5348cdaf567e1417c707a5')
```

Call the trigger_next_verification_event method with the verification
request id to trigger the next attempt to send the confirmation code:

```python
client.trigger_next_verification_event('00e6c3377e5348cdaf567e1417c707a5')
```

The verification request id comes from the call to the start_verification method.

### Checking a verification

Call the check_verification method with the verification request id and the
PIN code to complete the verification process:

```python
response = client.check_verification('00e6c3377e5348cdaf567e1417c707a5', code='1234')

if response['status'] == '0':
  print 'Verification complete, event_id=' + response['event_id']
else:
  print 'Error:', response['error_text']
```

The verification request id comes from the call to the start_verification method.
The PIN code is entered into your application by the user.

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


License
-------

This library is released under the [MIT License][license]

[signup]: https://dashboard.nexmo.com/sign-up?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library
[doc_sms]: https://docs.nexmo.com/messaging/sms-api?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library
[doc_verify]: https://docs.nexmo.com/verify/api-reference?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library
[doc_call]: https://docs.nexmo.com/voice/call?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library
[license]: LICENSE.txt
