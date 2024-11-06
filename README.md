# Vonage Server SDK for Python

<img src="https://developer.nexmo.com/images/logos/vbc-logo.svg" height="48px" alt="Vonage" />

[![PyPI version](https://badge.fury.io/py/vonage.svg)](https://badge.fury.io/py/vonage)
[![Build Status](https://github.com/Vonage/vonage-python-sdk/workflows/Build/badge.svg)](https://github.com/Vonage/vonage-python-sdk/actions)
[![Python versions supported](https://img.shields.io/pypi/pyversions/vonage.svg)](https://pypi.python.org/pypi/vonage)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)
![Total lines](https://sloc.xyz/github/vonage/vonage-python-sdk)

This is the Python server SDK to help you use Vonage APIs in your Python application. To use it you'll need a Vonage account. [Sign up for free on the Vonage site](https://ui.idp.vonage.com/ui/auth/registration).

### Contents:

- [Installation](#installation)
- [Migration Guides](#migration-guides)
- [Calling Vonage APIs](#calling-vonage-apis)
- [Usage](#usage)
- [Account API](#account-api)
- [Application API](#application-api)
- [HTTP Client](#http-client)
- [JWT Client](#jwt-client)
- [Messages API](#messages-api)
- [Network Number Verification API](#network-number-verification-api)
- [Network Sim Swap API](#network-sim-swap-api)
- [Number Insight API](#number-insight-api)
- [Numbers API](#numbers-api)
- [SMS API](#sms-api)
- [Subaccounts API](#subaccounts-api)
- [Users API](#users-api)
- [Verify API](#verify-api)
- [Verify API (Legacy)](#verify-api-legacy)
- [Video API](#video-api)
- [Voice API](#voice-api)
- [Vonage Utils Package](#vonage-utils-package)
- [Frequently Asked Questions](#frequently-asked-questions)
- [Contributing](#contributing)
- [License](#license)
- [Additional Resources](#additional-resources)

## Installation

It's recommended to create a new virtual environment to install the SDK. You can do this with

```bash
# Create the virtual environment
python3 -m venv venv

# Activate the virtual environment in Mac/Linux
. ./venv/bin/activate

# Or on Windows Command Prompt
venv\Scripts\activate
```

To install the Python SDK package using pip:

```bash
pip install vonage
```

To upgrade your installed client library using pip:

```bash
pip install vonage --upgrade
```

Alternatively, you can clone the repository via the command line, or by opening it on GitHub desktop.

## Migration Guides

### V3 to V4

This version of the Vonage Python SDK (4.x+) works very differently to the previous SDK. See [the v3 -> v4 migration guide](V3_TO_V4_SDK_MIGRATION_GUIDE.md) for help migrating your application code using v3 of the SDK to the new structure.

### OpenTok to Vonage Video API

This SDK includes support for the [Vonage Video API](https://developer.vonage.com/en/video/overview). If you have an application that uses OpenTok for video and want to migrate (which is highly recommended!) then [A migration guide is available here](video/OPENTOK_TO_VONAGE_MIGRATION.md) which will help you to migrate your applications to use Vonage Video.

## Calling Vonage APIs

The Vonage Python SDK is a monorepo, with separate packages for each API. When you install the Python SDK, you'll see there's a top-level package, `vonage`, and then specialised packages for every API class.

Most methods to call Vonage APIs are accessed through the top-level `vonage` package. Many require specific custom data models accessed though the specific Vonage package corresponding to the API you're trying to use.

For example, to send an SMS, you will access the SMS method from `vonage` and the `SmsMessage` object from the `vonage-sms` package. This looks something like this:

```python
from vonage_sms import SmsMessage, SmsResponse

message = SmsMessage(to='1234567890', from_='Acme Inc.', text='Hello, World!')
response: SmsResponse = vonage_client.sms.send(message) # vonage_client is an instance of `vonage.Vonage`

print(response.model_dump(exclude_unset=True))
```

## Usage

Many of the use cases require you to buy a Vonage Number, which you can [do in the Vonage Developer Dashboard](https://dashboard.nexmo.com/).

```python
from vonage import Vonage, Auth, HttpClientOptions

# Create an Auth instance
auth = Auth(api_key='your_api_key', api_secret='your_api_secret')

# Create HttpClientOptions instance
# (not required unless you want to change options from the defaults)
options = HttpClientOptions(api_host='api.nexmo.com', timeout=30)

# Create a Vonage instance
vonage = Vonage(auth=auth, http_client_options=options)
```

The Vonage class provides access to various Vonage APIs through its properties. For example, to use methods to call the SMS API:

```python
from vonage_sms import SmsMessage

message = SmsMessage(to='1234567890', from_='Vonage', text='Hello World')
response = client.sms.send(message)
print(response.model_dump_json(exclude_unset=True))
```

You can also access the underlying `HttpClient` instance through the `http_client` property:

```python
user_agent = vonage.http_client.user_agent
```

### Convert a Pydantic Model to Dict or Json

Most responses to API calls in the SDK are Pydantic models. To convert a Pydantic model to a dict, use `model.model_dump`. To convert to a JSON string, use `model.model_dump_json`

```python
response = vonage.api_package.api_call(...)

response_dict = response.model_dump()
response_json = response.model_dump_json()
```

## Account API

### Get Account Balance

```python
balance = vonage_client.account.get_balance()
print(balance)
```

### Top-Up Account

```python
response = vonage_client.account.top_up(trx='1234567890')
print(response)
```

### Update the Default SMS Webhook

This will return a Pydantic object (`SettingsResponse`) containing multiple settings for your account.

```python
settings: SettingsResponse = vonage_client.account.update_default_sms_webhook(
    mo_callback_url='https://example.com/inbound_sms_webhook',
    dr_callback_url='https://example.com/delivery_receipt_webhook',
)

print(settings)
```

### Get Service Pricing for a Specific Country

```python
from vonage_account import GetCountryPricingRequest

response = vonage_client.account.get_country_pricing(
    GetCountryPricingRequest(type='sms', country_code='US')
)
print(response)
```

### Get Service Pricing for All Countries

```python
response = vonage_client.account.get_all_countries_pricing(service_type='sms')
print(response)
```

### Get Service Pricing by Dialing Prefix

```python
from vonage_account import GetPrefixPricingRequest

response = client.account.get_prefix_pricing(
    GetPrefixPricingRequest(prefix='44', type='sms')
)
print(response)
```

### List Secrets Associated with the Account

```python
response = vonage_client.account.list_secrets()
print(response)
```

### Create a New Account Secret

```python
secret = vonage_client.account.create_secret('Mytestsecret12345')
print(secret)
```

### Get Information About One Secret

```python
secret = vonage_client.account.get_secret(MY_SECRET_ID)
print(secret)
```

### Revoke a Secret

Note: it isn't possible to revoke all account secrets, there must always be one valid secret. Attempting to do so will give a 403 error.

```python
client.account.revoke_secret(MY_SECRET_ID)
```

## Application API


### List Applications

With no custom options specified, this method will get the first 100 applications. It returns a tuple consisting of a list of `ApplicationData` objects and an int showing the page number of the next page of results.

```python
from vonage_application import ListApplicationsFilter, ApplicationData

applications, next_page = vonage_client.application.list_applications()

# With options
options = ListApplicationsFilter(page_size=3, page=2)
applications, next_page = vonage_client.application.list_applications(options)
```

### Create a New Application

```python
from vonage_application import ApplicationConfig

app_data = vonage_client.application.create_application()

# Create with custom options (can also be done with a dict)
from vonage_application import ApplicationConfig, Keys, Voice, VoiceWebhooks
voice = Voice(
    webhooks=VoiceWebhooks(
        event_url=VoiceUrl(
            address='https://example.com/event',
            http_method='POST',
            connect_timeout=500,
            socket_timeout=3000,
        ),
    ),
    signed_callbacks=True,
)
capabilities = Capabilities(voice=voice)
keys = Keys(public_key='MY_PUBLIC_KEY')
config = ApplicationConfig(
    name='My Customised Application',
    capabilities=capabilities,
    keys=keys,
)
app_data = vonage_client.application.create_application(config)
```

### Get an Application

```python
app_data = client.application.get_application('MY_APP_ID')
app_data_as_dict = app.model_dump(exclude_none=True)
```

### Update an Application

To update an application, pass config for the updated field(s) in an ApplicationConfig object

```python
from vonage_application import ApplicationConfig, Keys, Voice, VoiceWebhooks

config = ApplicationConfig(name='My Updated Application')
app_data = vonage_client.application.update_application('MY_APP_ID', config)
```

### Delete an Application

```python
vonage_client.applications.delete_application('MY_APP_ID')
```

## HTTP Client


```python
from vonage_http_client import HttpClient, HttpClientOptions
from vonage_http_client.auth import Auth

# Create an Auth instance
auth = Auth(api_key='your_api_key', api_secret='your_api_secret')

# Create HttpClientOptions instance
options = HttpClientOptions(api_host='api.nexmo.com', timeout=30)

# Create a HttpClient instance
client = HttpClient(auth=auth, http_client_options=options)

# Make a GET request
response = client.get(host='api.nexmo.com', request_path='/v1/messages')

# Make a POST request
response = client.post(host='api.nexmo.com', request_path='/v1/messages', params={'key': 'value'})
```

### Get the Last Request and Last Response from the HTTP Client

The `HttpClient` class exposes two properties, `last_request` and `last_response` that cache the last sent request and response.

```python
# Get last request, has type requests.PreparedRequest
request = client.last_request

# Get last response, has type requests.Response
response = client.last_response
```

### Appending to the User-Agent Header

The `HttpClient` class also supports appending additional information to the User-Agent header via the append_to_user_agent method:

```python
client.append_to_user_agent('additional_info')
```

### Changing the Authentication Method Used

The `HttpClient` class automatically handles JWT and basic authentication based on the Auth instance provided. It uses JWT authentication by default, but you can specify the authentication type when making a request:

```python
# Use basic authentication for this request
response = client.get(host='api.nexmo.com', request_path='/v1/messages', auth_type='basic')
```

### Catching errors

Error objects are exposed in the package scope, so you can catch errors like this:

```python
from vonage_http_client import HttpRequestError

try:
    client.post(...)
except HttpRequestError:
    ...
```

## JWT Client

This JWT Generator can be used implicitly, just by using the [Vonage Python SDK](https://github.com/Vonage/vonage-python-sdk) to make JWT-authenticated API calls.

It can also be used as a standalone JWT generator for use with Vonage APIs, like so:

### Import the `JwtClient` object

```python
from vonage_jwt import JwtClient
```

### Create a `JwtClient` object

```python
jwt_client = JwtClient(application_id, private_key)
```

### Generate a JWT using the provided application id and private key

```python
jwt_client.generate_application_jwt()
```

Optional JWT claims can be provided in a python dictionary:

```python
claims = {'jti': 'asdfzxcv1234', 'nbf': now + 100}
jwt_client.generate_application_jwt(claims)
```

## Verifying a JWT signature

You can use the `verify_jwt.verify_signature` method to verify a JWT signature is valid.

```python
from vonage_jwt import verify_signature

verify_signature(TOKEN, SIGNATURE_SECRET) # Returns a boolean
```

## Messages API


### How to Construct a Message

In order to send a message, you must construct a message object of the correct type. These are all found under `vonage_messages.models`.

```python
from vonage_messages.models import Sms

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
from vonage_messages.models import MessengerImage, MessengerOptions, MessengerResource

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
from vonage_messages.models import Sms

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

## Network Number Verification API

The Vonage Number Verification API uses Oauth2 authentication, which this SDK will also help you to do. Verifying a number has 3 stages:

1. Get an OIDC URL for use in your front-end application
2. Use this URL in your own application to get an authorization code
3. Make a Number Verification Request using this code to verify the number

This package contains methods to help with Steps 1 and 3.

### Get an OIDC URL

```python
from vonage_network_number_verification import CreateOidcUrl

url_options = CreateOidcUrl(
    redirect_uri='https://example.com/redirect',
    state='c9896ee6-4ff8-464c-b393-d56d6e638f88',
    login_hint='+990123456',
)

url = number_verification.get_oidc_url(url_options)
print(url)
```

Get your user's device to follow this URL and a code to use for number verification will be returned in the final redirect query parameters. Note: your user must be connected to their mobile network.

### Make a Number Verification Request

```python
from vonage_network_number_verification import NumberVerificationRequest

response = number_verification.verify(
    NumberVerificationRequest(
        code='code',
        redirect_uri='https://example.com/redirect',
        phone_number='+990123456',
    )
)
print(response.device_phone_number_verified)
```

## Network Sim Swap API

### Check if a SIM Has Been Swapped

```python
from vonage_network_sim_swap import SwapStatus
swap_status: SwapStatus = vonage_client.sim_swap.check(phone_number='MY_NUMBER')
print(swap_status.swapped)
```

### Get the Date of the Last SIM Swap

```python
from vonage_network_sim_swap import LastSwapDate
swap_date: LastSwapDate = vonage_client.sim_swap.get_last_swap_date
print(swap_date.last_swap_date)
```

## Number Insight API

### Make a Basic Number Insight Request

```python
from vonage_number_insight import BasicInsightRequest

response = vonage_client.number_insight.basic_number_insight(
    BasicInsightRequest(number='12345678900')
)

print(response.model_dump(exclude_none=True))
```

### Make a Standard Number Insight Request

```python
from vonage_number_insight import StandardInsightRequest

vonage_client.number_insight.standard_number_insight(
    StandardInsightRequest(number='12345678900')
)

# Optionally, you can get caller name information (additional charge) by setting the `cnam` parameter = True
vonage_client.number_insight.standard_number_insight(
    StandardInsightRequest(number='12345678900', cnam=True)
)
```

### Make an Asynchronous Advanced Number Insight Request

When making an asynchronous advanced number insight request, the API will return basic information about the request to you immediately and send the full data to the webhook callback URL you specify.

```python
from vonage_number_insight import AdvancedAsyncInsightRequest

vonage_client.number_insight.advanced_async_number_insight(
    AdvancedAsyncInsightRequest(callback='https://example.com', number='12345678900')
)
```

### Make a Synchronous Advanced Number Insight Request

```python
from vonage_number_insight import AdvancedSyncInsightRequest

vonage_client.number_insight.advanced_sync_number_insight(
    AdvancedSyncInsightRequest(number='12345678900')
)
```

## Numbers API

### List Numbers You Own

```python
numbers, count, next_page = vonage_client.numbers.list_owned_numbers()
print(numbers)
print(count)
print(next_page)

# With filtering
from vonage_numbers import ListOwnedNumbersFilter
numbers, count, next_page = vonage_client.numbers.list_owned_numbers(
    ListOwnedNumbersFilter(country='GB', size=3, index=2)
)

numbers, count, next_page_index = vonage_client.numbers.list_owned_numbers()
print(numbers)
print(count)
print(next_page_index)
```

### Search for Available Numbers

```python
from vonage_numbers import SearchAvailableNumbersFilter

numbers, count, next_page_index = vonage_client.numbers.search_available_numbers(
    SearchAvailableNumbersFilter(
        country='GB', size=10, pattern='44701', search_pattern=1
    )
)
print(numbers)
print(count)
print(next_page_index)
```

### Buy a Number

```python
from vonage_numbers import NumberParams

status = vonage_client.numbers.buy_number(NumberParams(country='GB', msisdn='447007000000'))
print(status)
```

### Cancel a number

```python
from vonage_numbers import NumberParams

status = vonage_client.numbers.cancel_number(NumberParams(country='GB', msisdn='447007000000'))
print(status)
```

### Update a Number

```python
from vonage_numbers import UpdateNumberParams

status = vonage_client.numbers.update_number(
    UpdateNumberParams(
        country='GB',
        msisdn='447007000000',
        mo_http_url='https://example.com',
        mo_smpp_sytem_type='inbound',
        voice_callback_type='tel',
        voice_callback_value='447008000000',
        voice_status_callback='https://example.com',
    )
)

print(status)
```

## SMS API

### Send an SMS

Create an `SmsMessage` object, then pass into the `Sms.send` method.

```python
from vonage_sms import SmsMessage, SmsResponse

message = SmsMessage(to='1234567890', from_='Acme Inc.', text='Hello, World!')
response: SmsResponse = vonage_client.sms.send(message)

print(response.model_dump(exclude_unset=True))
```

## Subaccounts API

### List Subaccounts

```python
response = vonage_client.subaccounts.list_subaccounts()
print(response.model_dump)
```

### Create Subaccount

```python
from vonage_subaccounts import SubaccountOptions

response = vonage_client.subaccounts.create_subaccount(
    SubaccountOptions(
        name='test_subaccount', secret='1234asdfA', use_primary_account_balance=False
    )
)
print(response)
```

### Modify a Subaccount

```python
from vonage_subaccounts import ModifySubaccountOptions

response = vonage_client.subaccounts.modify_subaccount(
    'test_subaccount',
    ModifySubaccountOptions(
        suspended=True,
        name='modified_test_subaccount',
    ),
)
print(response)
```

### List Balance Transfers

```python
from vonage_subaccounts import ListTransfersFilter

filter = {'start_date': '2023-08-07T10:50:44Z'}
response = vonage_client.subaccounts.list_balance_transfers(ListTransfersFilter(**filter))
for item in response:
    print(item.model_dump())
```

### Transfer Balance Between Subaccounts

```python
from vonage_subaccounts import TransferRequest

request = TransferRequest(
    from_='test_api_key', to='test_subaccount', amount=0.02, reference='A reference'
)
response = vonage_client.subaccounts.transfer_balance(request)
print(response)
```

### List Credit Transfers

```python
from vonage_subaccounts import ListTransfersFilter

filter = {'start_date': '2023-08-07T10:50:44Z'}
response = vonage_client.subaccounts.list_credit_transfers(ListTransfersFilter(**filter))
for item in response:
    print(item.model_dump())
```

### Transfer Credit Between Subaccounts

```python
from vonage_subaccounts import TransferRequest

request = TransferRequest(
    from_='test_api_key', to='test_subaccount', amount=0.02, reference='A reference'
)
response = vonage_client.subaccounts.transfer_balance(request)
print(response)
```

### Transfer a Phone Number Between Subaccounts

```python
from vonage_subaccounts import TransferNumberRequest

request = TransferNumberRequest(
    from_='test_api_key', to='test_subaccount', number='447700900000', country='GB'
)
response = vonage_client.subaccounts.transfer_number(request)
print(response)
```

## Users API

### List Users

With no custom options specified, this method will get the last 100 users. It returns a tuple consisting of a list of `UserSummary` objects and a string describing the cursor to the next page of results.

```python
from vonage_users import ListUsersRequest

users, _ = vonage_client.users.list_users()

# With options
params = ListUsersRequest(
    page_size=10,
    cursor=my_cursor,
    order='desc',
)
users, next_cursor = vonage_client.users.list_users(params)
```

### Create a New User

```python
from vonage_users import User, Channels, SmsChannel
user_options = User(
    name='my_user_name',
    display_name='My User Name',
    properties={'custom_key': 'custom_value'},
    channels=Channels(sms=[SmsChannel(number='1234567890')]),
)
user = vonage_client.users.create_user(user_options)
```

### Get a User

```python
user = client.users.get_user('USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b')
user_as_dict = user.model_dump(exclude_none=True)
```

### Update a User
```python
from vonage_users import User, Channels, SmsChannel, WhatsappChannel
user_options = User(
    name='my_user_name',
    display_name='My User Name',
    properties={'custom_key': 'custom_value'},
    channels=Channels(sms=[SmsChannel(number='1234567890')], whatsapp=[WhatsappChannel(number='9876543210')]),
)
user = vonage_client.users.update_user(id, user_options)
```

### Delete a User

```python
vonage_client.users.delete_user(id)
```

## Verify API

### Make a Verify Request

```python
from vonage_verify import VerifyRequest, SmsChannel
# All channels have associated models
sms_channel = SmsChannel(to='1234567890')
params = {
    'brand': 'Vonage',
    'workflow': [sms_channel],
}
verify_request = VerifyRequest(**params)

response = vonage_client.verify.start_verification(verify_request)
```

If using silent authentication, the response will include a `check_url` field with a url that should be accessed on the user's device to proceed with silent authentication. If used, silent auth must be the first element in the `workflow` list.

```python
silent_auth_channel = SilentAuthChannel(channel=ChannelType.SILENT_AUTH, to='1234567890')
sms_channel = SmsChannel(to='1234567890')
params = {
    'brand': 'Vonage',
    'workflow': [silent_auth_channel, sms_channel],
}
verify_request = VerifyRequest(**params)

response = vonage_client.verify.start_verification(verify_request)
```

### Check a Verification Code

```python
vonage_client.verify.check_code(request_id='my_request_id', code='1234')
```

### Cancel a Verification

```python
vonage_client.verify.cancel_verification('my_request_id')
```

### Trigger the Next Workflow Event

```python
vonage_client.verify.trigger_next_workflow('my_request_id')
```

## Verify API (Legacy)

### Make a Verify Request

```python
from vonage_verify_legacy import VerifyRequest
params = {'number': '1234567890', 'brand': 'Acme Inc.'}
request = VerifyRequest(**params)
response = vonage_client.verify_legacy.start_verification(request)
```

### Make a PSD2 (Payment Services Directive v2) Request

```python
from vonage_verify_legacy import Psd2Request
params = {'number': '1234567890', 'payee': 'Acme Inc.', 'amount': 99.99}
request = VerifyRequest(**params)
response = vonage_client.verify_legacy.start_verification(request)
```

### Check a Verification Code

```python
vonage_client.verify_legacy.check_code(request_id='my_request_id', code='1234')
```

### Search Verification Requests

```python
# Search for single request
response = vonage_client.verify_legacy.search('my_request_id')

# Search for multiple requests
response = vonage_client.verify_legacy.search(['my_request_id_1', 'my_request_id_2'])
```

### Cancel a Verification

```python
response = vonage_client.verify_legacy.cancel_verification('my_request_id')
```

### Trigger the Next Workflow Event

```python
response = vonage_client.verify_legacy.trigger_next_event('my_request_id')
```

### Request a Network Unblock

Note: Network Unblock is switched off by default. Contact Sales to enable the Network Unblock API for your account.

```python
response = vonage_client.verify_legacy.request_network_unblock('23410')
```

## Video API

You will use the custom Pydantic data models to make most of the API calls in this package. They are accessed from the `vonage_video.models` package.

### Generate a Client Token

```python
from vonage_video.models import TokenOptions

token_options = TokenOptions(session_id='your_session_id', role='publisher')
client_token = vonage_client.video.generate_client_token(token_options)
```

### Create a Session

```python
from vonage_video.models import SessionOptions

session_options = SessionOptions(media_mode='routed')
video_session = vonage_client.video.create_session(session_options)
```

### List Streams

```python
streams = vonage_client.video.list_streams(session_id='your_session_id')
```

### Get a Stream

```python
stream_info = vonage_client.video.get_stream(session_id='your_session_id', stream_id='your_stream_id')
```

### Change Stream Layout

```python
from vonage_video.models import StreamLayoutOptions

layout_options = StreamLayoutOptions(type='bestFit')
updated_streams = vonage_client.video.change_stream_layout(session_id='your_session_id', stream_layout_options=layout_options)
```

### Send a Signal

```python
from vonage_video.models import SignalData

signal_data = SignalData(type='chat', data='Hello, World!')
vonage_client.video.send_signal(session_id='your_session_id', data=signal_data)
```

### Disconnect a Client

```python
vonage_client.video.disconnect_client(session_id='your_session_id', connection_id='your_connection_id')
```

### Mute a Stream

```python
vonage_client.video.mute_stream(session_id='your_session_id', stream_id='your_stream_id')
```

### Mute All Streams

```python
vonage_client.video.mute_all_streams(session_id='your_session_id', excluded_stream_ids=['stream_id_1', 'stream_id_2'])
```

### Disable Mute All Streams

```python
vonage_client.video.disable_mute_all_streams(session_id='your_session_id')
```

### Start Captions

```python
from vonage_video.models import CaptionsOptions

captions_options = CaptionsOptions(language='en-US')
captions_data = vonage_client.video.start_captions(captions_options)
```

### Stop Captions

```python
from vonage_video.models import CaptionsData

captions_data = CaptionsData(captions_id='your_captions_id')
vonage_client.video.stop_captions(captions_data)
```

### Start Audio Connector

```python
from vonage_video.models import AudioConnectorOptions

audio_connector_options = AudioConnectorOptions(session_id='your_session_id', token='your_token', url='https://example.com')
audio_connector_data = vonage_client.video.start_audio_connector(audio_connector_options)
```

### Start Experience Composer

```python
from vonage_video.models import ExperienceComposerOptions

experience_composer_options = ExperienceComposerOptions(session_id='your_session_id', token='your_token', url='https://example.com')
experience_composer = vonage_client.video.start_experience_composer(experience_composer_options)
```

### List Experience Composers

```python
from vonage_video.models import ListExperienceComposersFilter

filter = ListExperienceComposersFilter(page_size=10)
experience_composers, count, next_page_offset = vonage_client.video.list_experience_composers(filter)
print(experience_composers)
```

### Get Experience Composer

```python
experience_composer = vonage_client.video.get_experience_composer(experience_composer_id='experience_composer_id')
```

### Stop Experience Composer

```python
vonage_client.video.stop_experience_composer(experience_composer_id='experience_composer_id')
```

### List Archives

```python
from vonage_video.models import ListArchivesFilter

filter = ListArchivesFilter(offset=2)
archives, count, next_page_offset = vonage_client.video.list_archives(filter)
print(archives)
```

### Start Archive

```python
from vonage_video.models import CreateArchiveRequest

archive_options = CreateArchiveRequest(session_id='your_session_id', name='My Archive')
archive = vonage_client.video.start_archive(archive_options)
```

### Get Archive

```python
archive = vonage_client.video.get_archive(archive_id='your_archive_id')
print(archive)
```

### Delete Archive

```python
vonage_client.video.delete_archive(archive_id='your_archive_id')
```

### Add Stream to Archive

```python
from vonage_video.models import AddStreamRequest

add_stream_request = AddStreamRequest(stream_id='your_stream_id')
vonage_client.video.add_stream_to_archive(archive_id='your_archive_id', params=add_stream_request)
```

### Remove Stream from Archive

```python
vonage_client.video.remove_stream_from_archive(archive_id='your_archive_id', stream_id='your_stream_id')
```

### Stop Archive

```python
archive = vonage_client.video.stop_archive(archive_id='your_archive_id')
print(archive)
```

### Change Archive Layout

```python
from vonage_video.models import ComposedLayout

layout = ComposedLayout(type='bestFit')
archive = vonage_client.video.change_archive_layout(archive_id='your_archive_id', layout=layout)
print(archive)
```

### List Broadcasts

```python
from vonage_video.models import ListBroadcastsFilter

filter = ListBroadcastsFilter(page_size=10)
broadcasts, count, next_page_offset = vonage_client.video.list_broadcasts(filter)
print(broadcasts)
```

### Start Broadcast

```python
from vonage_video.models import CreateBroadcastRequest, BroadcastOutputSettings, BroadcastHls, BroadcastRtmp

broadcast_options = CreateBroadcastRequest(session_id='your_session_id', outputs=BroadcastOutputSettings(
    hls=BroadcastHls(dvr=True, low_latency=False),
    rtmp=[
        BroadcastRtmp(
            id='test',
            server_url='rtmp://a.rtmp.youtube.com/live2',
            stream_name='stream-key',
        )
    ],
)
)
broadcast = vonage_client.video.start_broadcast(broadcast_options)
print(broadcast)
```

### Get Broadcast

```python
broadcast = vonage_client.video.get_broadcast(broadcast_id='your_broadcast_id')
print(broadcast)
```

### Stop Broadcast

```python
broadcast = vonage_client.video.stop_broadcast(broadcast_id='your_broadcast_id')
print(broadcast)
```

### Change Broadcast Layout

```python
from vonage_video.models import ComposedLayout

layout = ComposedLayout(type='bestFit')
broadcast = vonage_client.video.change_broadcast_layout(broadcast_id='your_broadcast_id', layout=layout)
print(broadcast)
```

### Add Stream to Broadcast

```python
from vonage_video.models import AddStreamRequest

add_stream_request = AddStreamRequest(stream_id='your_stream_id')
vonage_client.video.add_stream_to_broadcast(broadcast_id='your_broadcast_id', params=add_stream_request)
```

### Remove Stream from Broadcast

```python
vonage_client.video.remove_stream_from_broadcast(broadcast_id='your_broadcast_id', stream_id='your_stream_id')
```

### Initiate SIP Call

```python
from vonage_video.models import InitiateSipRequest, SipOptions, SipAuth

sip_request_params = InitiateSipRequest(
    session_id='your_session_id',
    token='your_token',
    sip=SipOptions(
        uri=f'sip:{vonage_number}@sip.nexmo.com;transport=tls',
        from_=f'test@vonage.com',
        headers={'header_key': 'header_value'},
        auth=SipAuth(username='1485b9e6', password='fL8jvi4W2FmS9som'),
        secure=False,
        video=False,
        observe_force_mute=True,
    ),
)
sip_call = vonage_client.video.initiate_sip_call(sip_request_params)
print(sip_call)
```

### Play DTMF into a call

```python
# Play into all connections
session_id = 'your_session_id'
digits = '1234#*p'

vonage_client.video.play_dtmf(session_id=session_id, digits=digits)

# Play into one connection
session_id = 'your_session_id'
digits = '1234#*p'
connection_id = 'your_connection_id'

vonage_client.video.play_dtmf(session_id=session_id, digits=digits, connection_id=connection_id)
```

## Voice API

### Create a Call

To create a call, you must pass an instance of the `CreateCallRequest` model to the `create_call` method. If supplying an NCCO, import the NCCO actions you want to use and pass them in as a list to the `ncco` model field.

```python
from vonage_voice.models import CreateCallRequest, Talk

ncco = [Talk(text='Hello world', loop=3, language='en-GB')]

call = CreateCallRequest(
    to=[{'type': 'phone', 'number': '1234567890'}],
    ncco=ncco,
    random_from_number=True,
)

response = vonage_client.voice.create_call(call)
print(response.model_dump())
```

### List Calls

```python
# Gets the first 100 results and the record_index of the
# next page if there's more than 100
calls, next_record_index = vonage_client.voice.list_calls()

# Specify filtering options
from vonage_voice.models import ListCallsFilter

call_filter = ListCallsFilter(
    status='completed',
    date_start='2024-03-14T07:45:14Z',
    date_end='2024-04-19T08:45:14Z',
    page_size=10,
    record_index=0,
    order='asc',
    conversation_uuid='CON-2be039b2-d0a4-4274-afc8-d7b241c7c044',
)

calls, next_record_index = vonage_client.voice.list_calls(call_filter)
```

### Get Information About a Specific Call

```python
call = vonage_client.voice.get_call('CALL_ID')
```

### Transfer a Call to a New NCCO

```python
ncco = [Talk(text='Hello world')]
vonage_client.voice.transfer_call_ncco('UUID', ncco)
```

### Transfer a Call to a New Answer URL

```python
vonage_client.voice.transfer_call_answer_url('UUID', 'ANSWER_URL')
```

### Hang Up a Call

End the call for a specified UUID, removing them from it.

```python
vonage_client.voice.hangup('UUID')
```

### Mute/Unmute a Participant

```python
vonage_client.voice.mute('UUID')
vonage_client.voice.unmute('UUID')
```

### Earmuff/Unearmuff a UUID

Prevent/allow a specified UUID participant to be able to hear audio.

```python
vonage_client.voice.earmuff('UUID')
vonage_client.voice.unearmuff('UUID')
```

### Play Audio Into a Call

```python
from vonage_voice.models import AudioStreamOptions

# Only the `stream_url` option is required
options = AudioStreamOptions(
    stream_url=['https://example.com/audio'], loop=2, level=0.5
)
response = vonage_client.voice.play_audio_into_call('UUID', options)
```

### Stop Playing Audio Into a Call

```python
vonage_client.voice.stop_audio_stream('UUID')
```

### Play TTS Into a Call

```python
from vonage_voice.models import TtsStreamOptions

# Only the `text` field is required
options = TtsStreamOptions(
    text='Hello world', language='en-ZA', style=1, premium=False, loop=2, level=0.5
)
response = voice.play_tts_into_call('UUID', options)
```

### Stop Playing TTS Into a Call

```python
vonage_client.voice.stop_tts('UUID')
```

### Play DTMF Tones Into a Call

```python
response = voice.play_dtmf_into_call('UUID', '1234*#')
```

## Vonage Utils Package

```python
from utils import format_phone_number, remove_none_values

# Use format_phone_number
try:
    formatted_number = format_phone_number('123-456-7890')
    print(formatted_number)
except (InvalidPhoneNumberError, InvalidPhoneNumberTypeError) as e:
    print(e)

# Use remove_none_values to remove null values from a Vonage API response when converting to a dictionary with the `asdict` method
from dataclasses import asdict

vonage_api_response = vonage.api.method()
cleaned_dict = asdict(my_dataclass, dict_factory=remove_none_values)
print(cleaned_dict)
```

## Frequently Asked Questions

### Supported APIs

The following is a list of Vonage APIs and whether the Python SDK provides support for them:

| API                   |  API Release Status  | Supported? |
| --------------------- | :------------------: | :--------: |
| Account API           | General Availability |     ✅     |
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
| Subaccounts API       | General Availability |     ✅     |
| Verify API            | General Availability |     ✅     |
| Verify API (Legacy)   | General Availability |     ✅     |
| Video API             | General Availability |     ✅     |
| Voice API             | General Availability |     ✅     |

### asyncio Support

[asyncio](https://docs.python.org/3/library/asyncio.html) is a library to write **concurrent** code using the **async/await** syntax.

We don't currently support asyncio in the Python SDK.

## Contributing

We :heart: contributions! But if you plan to work on something big or controversial, please contact us by raising an issue first!

We recommend working on `vonage-python-sdk` with a [virtualenv][virtualenv]. The following command will install all the Python dependencies you need to run the tests:

```bash
pip install -r requirements.txt
```

The tests are all written with pytest. You run them with:

```bash
pytest -v
```

We use [Black](https://black.readthedocs.io/en/stable/index.html) for code formatting, with our config in the `pyproject.toml` file. To ensure a PR follows the right format, you can set up and use our pre-commit settings with

```bash
pre-commit install
```

Then when you commit code, if it's not in the right format, it will be automatically fixed for you. After that, just commit again and everything should work as expected!

## License

This library is released under the [Apache License](license).

## Additional Resources

- [Vonage Video API Developer Documentation](https://developer.vonage.com/en/video/overview)
- [Link to the Vonage Python SDK](https://github.com/Vonage/vonage-python-sdk)
- [Join the Vonage Developer Community Slack](https://developer.vonage.com/en/community/slack)
- [Submit a Vonage Video API Support Request](https://api.support.vonage.com/hc/en-us)
