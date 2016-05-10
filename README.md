Nexmo Client Library for Python
===============================

[Installation](#installation) | [Usage](#usage) | [Examples](#examples) | [License](#license)

This is the Python client library for Nexmo's API. To use it you'll
need a Nexmo account. Sign up [for free at nexmo.com][signup].


Installation
------------

To install the Python client library using pip:

    $ pip install nexmo

Alternatively you can clone the repo or download the source.


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

### Sending A Message

Use [Nexmo's SMS API][doc_sms] to send an SMS message. 

Call the send_message method with a dictionary containing the message parameters. For example:

```python
import nexmo

client = nexmo.Client(key='YOUR-API-KEY', secret='YOUR-API-SECRET')

client.send_message({'from': 'Python', 'to': 'YOUR-NUMBER', 'text': 'Hello world'})
```


License
-------

This library is released under the [MIT License][license]

[signup]: http://nexmo.com?src=python-client-library
[doc_sms]: https://docs.nexmo.com/messaging/sms-api
[license]: LICENSE.txt
