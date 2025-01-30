# Vonage Messages Package

This package contains the code to use [Vonage's Messages API](https://developer.vonage.com/en/messages/overview) in Python.

## Usage

It is recommended to use this as part of the main `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`.

### How to Construct a Message

In order to send a message, you must construct a message object of the correct type.

```python
from vonage_messages import Sms

message = Sms(
    from_='Vonage APIs',
    to='1234567890',
    text='This is a test message sent from the Vonage Python SDK',
)
```

This message can now be sent with

```python
vonage_client.messages.send(message)
```

All possible message types from every message channel have their own message model. They are named following this rule: {Channel}{MessageType}, e.g. `Sms`, `MmsImage`, `RcsFile`, `MessengerAudio`, `WhatsappSticker`, `ViberVideo`, etc.

The different message models are listed at the bottom of the page.

Some message types have submodels with additional fields. In this case, import the submodels as well and use them to construct the overall options.

e.g.

```python
from vonage_messages import MessengerImage, MessengerOptions, MessengerResource

messenger = MessengerImage(
    to='1234567890',
    from_='1234567890',
    image=MessengerResource(url='https://example.com/image.jpg'),
    messenger=MessengerOptions(category='message_tag', tag='invalid_tag'),
)
```

### Send a message

To send a message, access the `Messages.send` method via the main Vonage object, passing in an instance of a subclass of `BaseMessage` like this:

```python
from vonage import Auth, Vonage
from vonage_messages import Sms

vonage_client = Vonage(Auth(application_id='my-application-id', private_key='my-private-key'))

message = Sms(
    from_='Vonage APIs',
    to='1234567890',
    text='This is a test message sent from the Vonage Python SDK',
)

vonage_client.messages.send(message)
```

### Mark a WhatsApp Message as Read

Note: to use this method, update the `api_host` attribute of the `vonage_http_client.HttpClientOptions` object to the API endpoint corresponding to the region where the WhatsApp number is hosted.

For example, to use the EU API endpoint, set the `api_host` attribute to 'api-eu.vonage.com'.

```python
from vonage import Vonage, Auth, HttpClientOptions

auth = Auth(application_id='MY-APP-ID', private_key='MY-PRIVATE-KEY')
options = HttpClientOptions(api_host='api-eu.vonage.com')

vonage_client = Vonage(auth, options)
vonage_client.messages.mark_whatsapp_message_read('MESSAGE_UUID')
```

### Revoke an RCS Message

Note: as above, to use this method you need to update the `api_host` attribute of the `vonage_http_client.HttpClientOptions` object to the API endpoint corresponding to the region where the WhatsApp number is hosted.

For example, to use the EU API endpoint, set the `api_host` attribute to 'api-eu.vonage.com'.

```python
from vonage import Vonage, Auth, HttpClientOptions

auth = Auth(application_id='MY-APP-ID', private_key='MY-PRIVATE-KEY')
options = HttpClientOptions(api_host='api-eu.vonage.com')

vonage_client = Vonage(auth, options)
vonage_client.messages.revoke_rcs_message('MESSAGE_UUID')
```

## Message Models

To send a message, instantiate a message model of the correct type as described above. This is a list of message models that can be used:

```
Sms
MmsImage, MmsVcard, MmsAudio, MmsVideo
RcsText, RcsImage, RcsVideo, RcsFile, RcsCustom
WhatsappText, WhatsappImage, WhatsappAudio, WhatsappVideo, WhatsappFile, WhatsappTemplate, WhatsappSticker, WhatsappCustom
MessengerText, MessengerImage, MessengerAudio, MessengerVideo, MessengerFile
ViberText, ViberImage, ViberVideo, ViberFile
```
