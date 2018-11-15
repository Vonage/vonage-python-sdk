Nexmo Client Library for Python
===============================

|PyPI version| |Build Status|

This is the Python client library for Nexmo's API. To use it you'll need
a Nexmo account. Sign up `for free at
nexmo.com <https://dashboard.nexmo.com/sign-up?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__.

-  `Installation <#installation>`__
-  `Usage <#usage>`__
-  `SMS API <#sms-api>`__
-  `Voice API <#voice-api>`__
-  `Verify API <#verify-api>`__
-  `Application API <#application-api>`__
-  `Coverage <#api-coverage>`__
-  `License <#license>`__

Installation
------------

To install the Python client library using pip:

::

    pip install nexmo

Alternatively, you can clone the repository:

::

    git clone git@github.com:Nexmo/nexmo-python.git

Usage
-----

Begin by importing the nexmo module:

.. code:: python

    import nexmo

Then construct a client object with your key and secret:

.. code:: python

    client = nexmo.Client(key=api_key, secret=api_secret)

For production, you can specify the ``NEXMO_API_KEY`` and
``NEXMO_API_SECRET`` environment variables instead of specifying the key
and secret explicitly.

For newer endpoints that support JWT authentication such as the Voice
API, you can also specify the ``application_id`` and ``private_key``
arguments:

.. code:: python

    client = nexmo.Client(application_id=application_id, private_key=private_key)

In order to check signatures for incoming webhook requests, you'll also
need to specify the ``signature_secret`` argument (or the
``NEXMO_SIGNATURE_SECRET`` environment variable).

If the argument ``signature_method`` is omitted, it will default to the md5 hash
algorithm. Otherwise, it will use the selected method as in md5, sha1, sha256 or
sha512 with hmac.

SMS API
-------

Send a text message
~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.send_message({'from': 'Python', 'to': 'YOUR-NUMBER', 'text': 'Hello world'})

    response = response['messages'][0]

    if response['status'] == '0':
      print('Sent message', response['message-id'])

      print('Remaining balance is', response['remaining-balance'])
    else:
      print('Error:', response['error-text'])

Docs:
`https://docs.nexmo.com/messaging/sms-api/api-reference#request <https://docs.nexmo.com/messaging/sms-api/api-reference#request?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Voice API
---------

Make a call
~~~~~~~~~~~

.. code:: python

    response = client.create_call({
      'to': [{'type': 'phone', 'number': '14843331234'}],
      'from': {'type': 'phone', 'number': '14843335555'},
      'answer_url': ['https://example.com/answer']
    })

Docs:
`https://docs.nexmo.com/voice/voice-api/api-reference#call\_create <https://docs.nexmo.com/voice/voice-api/api-reference#call_create?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Retrieve a list of calls
~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.get_calls()

Docs:
`https://docs.nexmo.com/voice/voice-api/api-reference#call\_retrieve <https://docs.nexmo.com/voice/voice-api/api-reference#call_retrieve?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Retrieve a single call
~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.get_call(uuid)

Docs:
`https://docs.nexmo.com/voice/voice-api/api-reference#call\_retrieve\_single <https://docs.nexmo.com/voice/voice-api/api-reference#call_retrieve_single?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Update a call
~~~~~~~~~~~~~

.. code:: python

    response = client.update_call(uuid, action='hangup')

Docs:
`https://docs.nexmo.com/voice/voice-api/api-reference#call\_modify\_single <https://docs.nexmo.com/voice/voice-api/api-reference#call_modify_single?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Verify API
----------

Start a verification
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.start_verification(number='441632960960', brand='MyApp')

    if response['status'] == '0':
      print 'Started verification request_id={request_id}'.format(request_id=response['request_id'])
    else:
      print('Error:', response['error_text'])

Docs:
`https://docs.nexmo.com/verify/api-reference/api-reference#vrequest <https://docs.nexmo.com/verify/api-reference/api-reference#vrequest?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

The response contains a verification request id which you will need to
store temporarily (in the session, database, url etc).

Check a verification
~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.check_verification('00e6c3377e5348cdaf567e1417c707a5', code='1234')

    if response['status'] == '0':
      print 'Verification complete, event_id={event_id}'.format(event_id=response['event_id'])
    else:
      print('Error:', response['error_text'])

Docs:
`https://docs.nexmo.com/verify/api-reference/api-reference#check <https://docs.nexmo.com/verify/api-reference/api-reference#check?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

The verification request id comes from the call to the
start\_verification method. The PIN code is entered into your
application by the user.

Cancel a verification
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    client.cancel_verification('00e6c3377e5348cdaf567e1417c707a5')

Docs:
`https://docs.nexmo.com/verify/api-reference/api-reference#control <https://docs.nexmo.com/verify/api-reference/api-reference#control?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Trigger next verification step
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    client.trigger_next_verification_event('00e6c3377e5348cdaf567e1417c707a5')

Docs:
`https://docs.nexmo.com/verify/api-reference/api-reference#control <https://docs.nexmo.com/verify/api-reference/api-reference#control?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Application API
---------------

Create an application
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.create_application(name='Example App', type='voice', answer_url=answer_url)

Docs:
`https://docs.nexmo.com/tools/application-api/api-reference#create <https://docs.nexmo.com/tools/application-api/api-reference#create?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Retrieve a list of applications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.get_applications()

Docs:
`https://docs.nexmo.com/tools/application-api/api-reference#list <https://docs.nexmo.com/tools/application-api/api-reference#list?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Retrieve a single application
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.get_application(uuid)

Docs:
`https://developer.nexmo.com/api/application#retrieve-an-application <https://developer.nexmo.com/api/application#retrieve-an-application>`__

Update an application
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.update_application(uuid, answer_method='POST')

Docs:
`https://docs.nexmo.com/tools/application-api/api-reference#update <https://docs.nexmo.com/tools/application-api/api-reference#update?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Delete an application
~~~~~~~~~~~~~~~~~~~~~

.. code:: python

    response = client.delete_application(uuid)

Docs:
`https://docs.nexmo.com/tools/application-api/api-reference#delete <https://docs.nexmo.com/tools/application-api/api-reference#delete?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Validate webhook signatures
---------------------------

.. code:: python

    client = nexmo.Client(signature_secret='secret')

    if client.check_signature(request.query):
      # valid signature
    else:
      # invalid signature


    or by using signature method via POST:

    client = nexmo.Client(signature_secret='secret', signature_method='sha256')

    if client.check_signature(request.body.decode()):
      # valid signature
    else:
      # invalid signature

Docs:
`https://docs.nexmo.com/messaging/signing-messages <https://docs.nexmo.com/messaging/signing-messages?utm_source=DEV_REL&utm_medium=github&utm_campaign=python-client-library>`__

Note: you'll need to contact support@nexmo.com to enable message signing
on your account before you can validate webhook signatures.

JWT parameters
--------------

By default, the library generates short-lived tokens for JWT
authentication.

Use the auth method to specify parameters for a longer life token or to
specify a different token identifier:

.. code:: python

    client.auth(nbf=nbf, exp=exp, jti=jti)

API Coverage
------------

-  Account

   -  [X] Balance
   -  [X] Pricing
   -  [X] Settings
   -  [X] Top Up
   -  [X] Numbers

      -  [X] Search
      -  [X] Buy
      -  [X] Cancel
      -  [X] Update

-  Number Insight

   -  [X] Basic
   -  [X] Standard
   -  [X] Advanced
   -  [ ] Webhook Notification

-  Verify

   -  [X] Verify
   -  [X] Check
   -  [X] Search
   -  [X] Control

-  Messaging

   -  [X] Send
   -  [ ] Delivery Receipt
   -  [ ] Inbound Messages
   -  [X] Search

      -  [X] Message
      -  [X] Messages
      -  [X] Rejections

   -  [X] US Short Codes

      -  [X] Two-Factor Authentication
      -  [X] Event Based Alerts

         -  [X] Sending Alerts
         -  [X] Campaign Subscription Management

-  Voice

   -  [X] Outbound Calls
   -  [ ] Inbound Call
   -  [X] Text-To-Speech Call
   -  [X] Text-To-Speech Prompt

License
-------

This library is released under the `MIT License <LICENSE.txt>`__

.. |PyPI version| image:: https://badge.fury.io/py/nexmo.svg
   :target: https://badge.fury.io/py/nexmo
.. |Build Status| image:: https://api.travis-ci.org/Nexmo/nexmo-python.svg?branch=master
   :target: https://travis-ci.org/Nexmo/nexmo-python
