# Vonage Python SDK v3 to v4 Migration Guide

This is a guide to help you migrate from using v3 of the Vonage Python SDK to using the new v4 `vonage` package. It has feature parity with the v3 package and contains many enhancements and structural changes. We will only be supporting v4 from the time of its full release.

The Vonage Python SDK (`vonage`) contains methods and data models to help you use many of Vonage's APIs. It also includes support for the new mobile network APIs announced by Vonage.

## Contents

- [Structural Changes and Enhancements](#structural-changes-and-enhancements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Accessing API Methods](#accessing-api-methods)
- [Accessing API Data Models](#accessing-api-data-models)
- [Response Objects](#response-objects)
- [Error Handling](#error-handling)
- [General API Changes](#general-API-changes)
- [Specific API Changes](#specific-api-changes)
- [Method Name Changes](#method-name-changes)
- [Additional Resources](#additional-resources)

## Structural Changes and Enhancements

Here are some key changes to the SDK:

1. v4 of the Vonage Python SDK now uses a monorepo structure, with different packages for calling different Vonage APIs all using common code. You don't need to install the different packages directly as the top-level `vonage` package pulls them in and provides a common and consistent way to access methods.
2. The v4 SDK makes heavy use of [Pydantic data models](https://docs.pydantic.dev/latest/) to make it easier to call Vonage APIs and parse the results. This also enforces correct typing and makes it easier to pass the right objects to Vonage.
3. Docstrings have been added to methods and data models across the whole SDK to increase quality-of-life developer experience and make in-IDE development easier.
4. Many new custom errors have been added for finer-grained debugging. Error objects now contain more information and error messages give more information and context.
5. Support has been added for all [Vonage Video API](https://developer.vonage.com/en/video/overview) features, bringing it to feature parity with the OpenTok package. See [the OpenTok -> Vonage Video migration guide](video/OPENTOK_TO_VONAGE_MIGRATION.md) for migration assistance. If you're using OpenTok, migration to use v4 of the Vonage Python SDK rather than the `opentok` Python package is highly recommended.
6. APIs that have been deprecated by Vonage, e.g. Meetings API, have not been implemented in v4. Objects deprecated in v3 of the SDK have also not been implemented in v4.

## Installation

The most common way to use the new v4 package is by installing the top-level `vonage` package, similar to how you would install v3. The difference is that the new package will install the other Vonage API packages as dependencies.

To install the Python SDK package using pip:

```bash
pip install vonage
```

To upgrade your installed client library using pip:

```bash
pip install vonage --upgrade
```

You will notice that the dependent Vonage packages have been installed as well.

## Configuration

To get started with the v4 SDK, you'll need to initialize an instance of the `vonage.Vonage` class. This can then be used to access API methods. You need to provide authentication information and can optionally provide configuration options for the HTTP Client used to make requests to Vonage APIs. This section will break all of this down then provide an example.

### Authentication

Depending on the Vonage API you want to use, you'll use different forms of authentication. You'll need to provide either an API key and secret or the ID of a Vonage Application and its corresponding private key. This is done by initializing an instance of `vonage.Auth`.

```python
from vonage import Auth

# API key/secret authentication
auth = Auth(api_key='your_api_key', api_secret='your_api_secret')

# Application ID/private key authentication
auth = Auth(application_id='your_api_key', private_key='your_api_secret')
```

This `auth` can then be used when initializing an instance of `vonage.Vonage` (example later in this section).

### Setting HTTP Client Options

The HTTP client used to make requests to Vonage comes with sensible default options, but if you need to change any of these, create a `vonage.HttpClientOptions` object and pass that in to `vonage.Vonage` when you create the object.

```python
# Create HttpClientOptions instance with some non-default settings
options = HttpClientOptions(api_host='new-api-host.example.com', timeout=100)
```

### Example

Putting all this together, to set up an instance of the `vonage.Vonage` class to call Vonage APIs, do this:

```python
from vonage import Vonage, Auth, HttpClientOptions

# Create an Auth instance
auth = Auth(api_key='your_api_key', api_secret='your_api_secret')

# Create HttpClientOptions instance
# (not required unless you want to change options from the defaults)
options = HttpClientOptions(api_host='new-api-host.example.com', timeout=100)

# Create a Vonage instance
vonage = Vonage(auth=auth, http_client_options=options)
```

## Accessing API Methods

To access methods relating to Vonage APIs, you'll create an instance of the `vonage.Vonage` class and access them via named attributes, e.g. if you have an instance of `vonage.Vonage` called `vonage_client`, use this syntax:

```python
vonage_client.vonage_api.api_method(...)

# E.g.
vonage_client.video.create_session(...)
```

This is very similar to the v3 SDK.

## Accessing API Data Models

Unlike the methods to call each Vonage API, the data models and errors specific to each API are not accessed through the `vonage` package, but are instead accessed through the specific API package.

For most APIs, data models and errors can be accessed from the top level of the API package, e.g. to send a Verify request, do this:

```python
from vonage_verify import VerifyRequest, SmsChannel

sms_channel = SmsChannel(to='1234567890')
verify_request = VerifyRequest(brand='Vonage', workflow=[sms_channel])

response = vonage_client.verify.start_verification(verify_request)
print(response)
```

However, some APIs with a lot of models have them located under the `<vonage_api_package>.models` package, e.g. `vonage-messages`, `vonage-voice` and `vonage-video`. To access these, simply import from `<vonage_api_package>.models`, e.g. to send an image via Facebook Messenger do this:

```python
from vonage_messages.models import MessengerImage, MessengerOptions, MessengerResource

messenger_image_model = MessengerImage(
    to='1234567890',
    from_='1234567890',
    image=MessengerResource(url='https://example.com/image.jpg'),
    messenger=MessengerOptions(category='message_tag', tag='invalid_tag'),
)

vonage_client.messages.send(message)
```

## Response Objects

In v3 of the SDK, the APIs returned Python dictionaries. In v4, almost all responses are now deserialized from the returned JSON into Pydantic models. Response data models are accessed in the same way as the other data models above and are also fully documented with useful docstrings.

If you want to convert the Pydantic responses into dictionaries, just use the `model_dump` method on the response. For example:

```python
from vonage_account import SettingsResponse

settings: SettingsResponse = vonage_client.account.update_default_sms_webhook(
    mo_callback_url='https://example.com/sms_webhook',
    dr_callback_url='https://example.com/delivery_receipt_webhook',
)

print(settings.model_dump())
```

Response fields are also converted into snake_case where applicable, so as to be more pythonic. This means they won't necessarily match the API one-to-one.

## Error Handling

In v3 of the SDK, most HTTP client errors gave a general `HttpClientError`. Errors in v4 inherit from the general `VonageError` but are more specific and finer-grained, E.g. a `RateLimitedError` when the SDK receives an HTTP 429 response.

These errors will have a descriptive message and will also include the response object returned to the SDK, accessed by `HttpClientError.response` etc.

Some API packages have their own errors for specific cases too.

For older Vonage APIs that always return an HTTP 200, error handling logic has been included to give a similar experience to the newer APIs.

## General API Changes

In v3, you access `vonage.Client`. In v4, it's `vonage.Vonage`.

The methods to get and set host attributes in v3 e.g. `vonage.Client.api_host` have been removed. You now get these options in v4 via the `vonage.Vonage.http_client`. Set these options in v4 by adding the options you want to the `vonage.HttpClientOptions` data model when initializing a `vonage.Vonage` object.

## Specific API Changes

### Video API

Methods have been added to help you work with the Live Captions, Audio Connector and Experience Composer APIs. See the [Video API samples](video/README.md) for more information.

### Voice API

Methods have been added to help you moderate a voice call:

- `voice.hangup`
- `voice.mute`
- `voice.unmute`
- `voice.earmuff`
- `voice.unearmuff`

See the [Voice API samples](voice/README.md) for more information.

### Network Number Verification API

The process for verifying a number using the Network Number Verification API has been simplified. In v3 it was required to exchange a code for a token then use this token in the verify request. In v4, these steps are combined so both functions are taken care of in the `NetworkNumberVerification.verify` method.

### Verify API Name Changes

The functionality previously named "Verify V2" in v3 of the SDK has been renamed "Verify", along with associated methods. The old Verify product in v3 has been renamed "Verify Legacy".

Verify v2 functionality is now accessed from `vonage_client.verify` in v4, which exposes the `vonage_verify.Verify` class. The legacy Verify v1 objects are accessed from `vonage_client.verify_legacy` in v4, in the new package `vonage-verify-legacy`.

### SMS API

Code for signing/verifying signatures of SMS messages that was in the `vonage.Client` class in v3 has been moved into the `vonage-http-client` package in v4. This can be accessed via the `vonage` package as we import the `vonage-http-client.Auth` class into its namespace.

Old method -> new method
`vonage.Client.sign_params` -> `vonage.Auth.sign_params`
`vonage.Client.check_signature` -> `vonage.Auth.check_signature`

## Method Name Changes

Some methods from v3 have had their names changed in v4. Assuming you access all methods from the `vonage.Vonage` class in v4 with `vonage.Vonage.api_method` or the `vonage.Client` class in v3 with `vonage.Client.api_method`, this table details the changes:

| 3.x Method Name | 4.x Method Name |
|-----------------|-----------------|
| `account.topup` | `account.top_up` |
| `messages.send_message` | `messages.send` |
| `messages.revoke_outbound_rcs_message` | `messages.revoke_rcs_message` |
| `number_insight.get_basic_number_insight` | `number_insight.basic_number_insight` |
| `number_insight.get_standard_number_insight` | `number_insight.standard_number_insight` |
| `number_insight.get_advanced_number_insight` | `number_insight.advanced_sync_number_insight` |
| `number_insight.get_async_advanced_number_insight` | `number_insight.advanced_async_number_insight` |
| `numbers.get_account_numbers` | `numbers.list_owned_numbers` |
| `numbers.get_available_numbers` | `numbers.search_available_numbers` |
| `sms.send_message` | `sms.send` |
| `verify.start_verification` | `verify_legacy.start_verification` |
| `verify.psd2` | `verify_legacy.start_psd2_verification` |
| `verify.check` | `verify_legacy.check_code` |
| `verify.search` | `verify_legacy.search` |
| `verify.cancel_verification` | `verify_legacy.cancel_verification` |
| `verify.trigger_next_event` | `verify_legacy.trigger_next_event` |
| `verify.request_network_unblock` | `verify_legacy.request_network_unblock` |
| `verify2.new_request` | `verify.start_verification` |
| `verify2.check_code` | `verify.check_code` |
| `verify2.cancel_verification` | `verify.cancel_verification` |
| `verify2.trigger_next_workflow` | `verify.trigger_next_workflow` |
| `video.set_stream_layout` | `video.change_stream_layout` |
| `video.create_archive` | `video.start_archive` |
| `video.create_sip_call` | `video.initiate_sip_call` |
| `voice.get_calls` | `voice.list_calls` |
| `voice.update_call` | `voice.transfer_call_ncco` and `voice.transfer_call_answer_url` |
| `voice.send_audio` | `voice.play_audio_into_call` |
| `voice.stop_audio` | `voice.stop_audio_stream` |
| `voice.send_speech` | `voice.play_tts_into_call` |
| `voice.stop_speech` | `voice.stop_tts` |
| `voice.send_dtmf` | `voice.play_dtmf_into_call` |

## Additional Resources

- [Link to the Vonage Python SDK](https://github.com/Vonage/vonage-python-sdk)
- [Join the Vonage Developer Community Slack](https://developer.vonage.com/en/community/slack)
- [Submit a Vonage API Support Request](https://api.support.vonage.com/hc/en-us)