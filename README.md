nexmo
=====


Python client for the [Nexmo API](https://docs.nexmo.com/).


Installation
------------

    $ pip install nexmo


Sending a message
-----------------

Construct a nexmo.Client object with your API credentials and call
the send_message method to send a message. For example:

```python
import nexmo

client = nexmo.Client(key='YOUR-API-KEY', secret='YOUR-API-SECRET')

client.send_message({'from': 'Python', 'to': 'YOUR-NUMBER', 'text': 'Hello world'})
```

The Nexmo documentation contains a [list of error codes](https://docs.nexmo.com/index.php/sms-api/send-message#response_code)
which may be useful for debugging errors. Remember that phone numbers
should be specified in international format, and other country specific
restrictions may apply (e.g. US messages must originate from either a
pre-approved long number or short code).


Production environment variables
--------------------------------

Best practice for storing credentials for external services in production is
to use environment variables, as described by [12factor.net/config](http://12factor.net/config).
The nexmo.Client constructor defaults to extracting the API credentials it
needs from the NEXMO_API_KEY and NEXMO_API_SECRET environment variables if
the key/secret arguments were not specified explicitly.
