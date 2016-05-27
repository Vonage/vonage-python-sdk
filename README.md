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

message = response['messages'][0]

if message['status'] == '0':
  print 'sent message', message['message-id'], 'remaining balance is', message['remaining-balance']
else:
  print 'error:', message['error-text']
```

### Fetching a message

You can retrieve a message log from the API using the ID of the message:

```python
message = client.get_message('02000000DA7C52E7')

print 'The body of the message was:', message['body']
```


License
-------

This library is released under the [MIT License][license]

[signup]: https://dashboard.nexmo.com/sign-up?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library
[doc_sms]: https://docs.nexmo.com/messaging/sms-api?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library
[license]: LICENSE.txt
