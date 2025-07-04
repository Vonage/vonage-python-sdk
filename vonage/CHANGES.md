# 4.5.0
- vonage-messages: add an optional "failover" property to `vonage_messages.Messages.send`

# 4.4.3
- vonage-number-insight: use basic header auth instead of request body auth

# 4.4.2
- vonage-sms: make returned response fields optional

# 4.4.1
- Update some Voice API parameters

# 4.4.0
Vonage Voice Package:
- Add new `headers` and `standard_headers` options to the `Sip` data model
- Add new `standardHeaders` option to the `SipEndpoint` NCCO model
- Add check for invalid hostnames when downloading a recording with `Voice.download_recording`
- Allow the `CreateCallRequest` model to accept a SIP URI as well as a phone number in the `from_` field

# 4.3.0
- Make all models originally accessed by `vonage_voice.models.***` available at the top level of the package, i.e. `vonage_voice.***`
- Make all models originally accessed by `vonage_video.models.***` available at the top level of the package, i.e. `vonage_video.***`
- Make all models originally accessed by `vonage_messages.models.***` available at the top level of the package, i.e. `vonage_messages.***`

# 4.2.0
- Add new `max_bitrate` field for Video API archives
- Fix a bug with error types
- Update an outdated Voice class type hint

# 4.1.2
- Remove max length constraint in Voice API for webhook URIs

# 4.1.1
- Include new package versions

# 4.1.0
- Add support for API key/secret header authentication for the Messages and Verify APIs (JWT is the default and recommended method)
- Add `Voice.get_recording` method to get call recordings
- Add `Voice.verify_signature` method to expose the verification functionality from `vonage-jwt`
- Add backoff exponential timeout increase for HTTP request retries
- Add automatic retries for `RemoteDisconnected` exceptions
- Add new `http_client.FileStreamingError` exception type

# 4.0.0
A complete, ground-up rewrite of the SDK.
Key changes:
- Monorepo structure, with each API under separate packages
- Support for Python 3.9+
- Feature parity with v3
- Add support for the new network APIs - the [Vonage Sim Swap Network API](https://developer.vonage.com/en/sim-swap/overview) and the [Vonage Number Verification Network API](https://developer.vonage.com/en/number-verification/overview)
- Usage of data models throughout
- Many new custom errors, improved error data models and error messages
- Docstrings for methods and data models across the whole SDK to increase quality-of-life developer experience and make in-IDE development easier
- Use of Pydantic to enforce correct typing throughout
- Add support for all [Vonage Video API](https://developer.vonage.com/en/video/overview) features
- Add `http_client` property to each module that has an HTTP Client, e.g. Voice, Sms, Verify
- Add `last_request` and `last_response` properties to the HTTP Client for easier debugging
- Migrated the Vonage JWT package into the monorepo
- Rename `Verify` -> `VerifyLegacy` and `VerifyV2` -> `Verify`

# 3.17.4
- Drop support for Python 3.8, add support for 3.13

# 3.17.3
- Fix bug in JWT generator

# 3.17.2
- Update `vonage-jwt` dependency version to fix JWT timeout issue

# 3.17.1
- Add "mark WhatsApp message as read" option for Messages API

# 3.17.0
- Add RCS message type option for Messages API
- Add "revoke RCS message" option

# 3.16.1
- Fix video client token option
- Fix typos in README
- Bump minimum versions for dependencies with fixed vulnerabilities

# 3.16.0
- Add support for the [Vonage Number Verification API](https://developer.vonage.com/number-verification/overview)

# 3.15.0
- Add support for the [Vonage Sim Swap API](https://developer.vonage.com/en/sim-swap/overview)

# 3.14.0
- Add publisher-only as a valid Video API client token role

# 3.13.1
- Fix content-type incorrect serialization

# 3.13.0
- Migrating to use Pydantic v2 as a dependency

# 3.12.0
- Add support for the [Vonage Video API](https://developer.vonage.com/en/video/overview)

# 3.11.1
- Add checks for silent auth workflow optional parameters `redirect_url` and `sandbox`

# 3.11.0
- Add method to check JWT signatures of Voice API webhooks: `vonage.Voice.verify_signature`

# 3.10.0
- Indicating support for Python 3.12

# 3.9.1
- Updating Meetings API url to a `/v1` endpoint

# 3.9.0
- Dropped support for Python 3.7 as it's end-of-life and no longer receiving security updates

# 3.8.0
- Adding support for the [Users component of the Vonage Application API](https://developer.vonage.com/en/api/application.v2#User)

# 3.7.1
- Fixing dependency version to a specific major version

# 3.7.0
- Adding support for the [Vonage Meetings API](https://developer.vonage.com/en/meetings/overview)
- Adding partial support for the [Vonage Proactive Connect API](https://developer.vonage.com/en/proactive-connect/overview) - supporting API methods relating to `lists`, `items` and `events`
- Returning a more descriptive (non-internal) error message if invalid values are provided for `application_id` and/or `private_key` when instantiating a Vonage client object

# 3.6.0
- Adding support for the [Vonage Subaccounts API](https://developer.vonage.com/en/account/subaccounts/overview)

# 3.5.2
- Using the [Vonage JWT Generator](https://github.com/Vonage/vonage-python-jwt) instead of `PyJWT` for generating JWTs.
- Other internal refactoring and enhancements

# 3.5.1
- Updating the internal use of the `fraud_check` parameter in the Vonage Verify V2 API

# 3.5.0
- Adding support for V2 of the Vonage Verify API
    - Multiple authentication channels are supported (sms, voice, email, whatsapp, whatsapp interactive messages and silent authentication)
    - Using fallback channels is now possible in case verification methods fail
    - You can now customise the verification code that is sent, or even specify your own custom code
- Adding `advancedMachineDetection` functionality to the NCCO builder for the Vonage Voice API

# 3.4.0
- Internal refactoring changes
- Using header authentication for the Numbers API

# 3.3.0
- Updated Messages API:
    - Added new messaging channels for Viber Service Messages (`video`, `file`)
    - Added new WhatsApp `sticker` message channel
    - Increased `client_ref` max value to 100 characters
- Deprecated `pay` action in the NCCO builder as it is being removed by Vonage

# 3.2.2
- Fixing a bug on Windows

# 3.2.1
- Fixing an import bug

# 3.2.0
- Adding an NCCO Builder to make it easier to work with NCCOs when using the Voice API
- Individual NCCO Actions can be created as Pydantic models, which can be built into an NCCO via the `Ncco.build_ncco` method

# 3.1.0
- Supporting Python 3.11
- Upgrading some old dependencies

# 3.0.2
- Bugfix in `messages.py` where authentication method was not being checked for correctly, throwing an error when using header auth.

# 3.0.1
- Fixed bug where a JWT was created globally and could expire. Now a new JWT is generated when a request is made.
- Fixed bug where timeout was not passed to session object.

# 3.0.0
Breaking changes:
- Removed deprecated methods from `client.py` that are now available in specific modules related to each of the available Vonage APIs. E.g. to call the number insight API, the methods are now called in this way: `client.number_insight.get_basic_number_insight(...)`, or by instantiating the `NumberInsight` class directly: `ni = vonage.NumberInsight(client)`, `ni.get_basic_number_insight(...)` etc.
- Removed automatic client creation when instantiating an `sms`, `voice` or `verify` object. You can now use these APIs from a client instance you create (e.g. `client.sms.send_message()`) or pass in a client to the API class to create it (e.g. `sms = vonage.Sms(client)`), as has been the case since v2.7.0 of the SDK.
- Removed methods to call the Message Search API, which has been retired by Vonage.
- Removed deprecated voice and number insight methods from `voice.py` (`initiate_call, initiate_tts_call and initiate_tts_prompt_call`) and `number_insight.py` (`request_number_insight`).
- Renamed the `Account.delete_secret()` method to `revoke_secret()` to bring it in line with what is described in our documentation.

Deprecations:
- Deprecated the ApplicationV2 class and created an Application class with the same methods to bring the naming in line with other classes. This can be called from the client object with `client.application.create_application(...)` etc. or directly with `application = vonage.Application(client)`, `application.create_application(...)` etc.
- Deprecated old Pricing API methods `get_sms_pricing` and `get_voice_pricing`.
- Deprecated Redact class as it's a dev preview product that's unsupported in the SDK and will be removed in a later release.

Enhancements:
- Added `get_all_countries_pricing` method to `Account` object.
- Added a `type` parameter for pricing calls, so `sms` or `voice` pricing can now be chosen.
- Added `max_retries`, `timeout`, `pool_connections` and `pool_maxsize` optional keyword arguments to the `Client` class, which can now be specified on instantiation and used in the API calls made with the client.

# 2.8.0
- Added Messages API v1.0 support. Messages API can now be used by calling the `client.messages.send_message()` method.

# 2.7.0
- Moved some client methods into their own classes: `account.py, application.py,
message_search.py, number_insight.py, numbers.py, short_codes.py, ussd.py`
- Deprecated the corresponding client methods. These will be removed in a major release that's coming soon.
- Client now instantiates a class object for each API when it is created, e.g. `vonage.Client(key="mykey", secret="mysecret")`
instantiates instances of `Account`, `Sms`, `NumberInsight` etc. These instances can now be called directly from `Client`, e.g.
```
client = vonage.Client(key="mykey", secret="mysecret")

print(f"Account balance is: {client.account.get_balance()}")

print("Sending an SMS")
client.sms.send_message(
    "from": "Vonage",
    "to": "SOME_PHONE_NUMBER",
    "text": "Hello from Vonage's SMS API"
)

```

# 2.6.x

- Dropped support for Python 3.6 and below
- Now supporting currently supported stable versions of Python, i.e. Python 3.7-3.10
- Internal refactoring and enhancements
- Adding default `max_retries` option to the `BasicAuthenticationServer` constructor, specifying optional parameters

# 2.5.5

- Support for Independent SMS, Voice and Verify APIs with tests as well as current client methods
- Getters/Setters to extract/rewrite custom attributes
- PSD2 Verification support
- Dropping support for Python 2.7
- Roadmap to better error handling
- Supporting Python 3.8

# 2.4.0

- Application V2 API added under `Client.application_v2`
- Existing application methods under `Client` are now deprecated.

# 2.3.0

- Explicit parameter list for the `nexmo.Client` constructor. **This may cause errors in code passing incorrect or spurious arguments to the Client constructor.**
- Secret Management
- Support for Authorization header authentication.

# 2.2.0

- Add support for `redact_transaction`.

# 2.1.0

- Add support for `get_recording`
- Add support for SMS conversion
- Add debug logging for most calls, under the 'nexmo' logger.
- Internal refactoring (affects only private methods.)

# 2.0.0

- Drop support for Python 3.3 (in line with the cryptography library we depend upon)
- Ensure timestamp is added the params list if signing requests
- Avoid value injection in signature auth.
- Add support for different hashes for signature generation (thanks @trancee!)
- Tests ported to pytest

# 1.5.0

- Add ability to provide a file path as private_key param no the nexmo.Client constructor

- Add send/stop endpoints for audio/speech/dtmf

- Add new number insight endpoints

# 1.4.0

- Add new Voice API call methods

- Add Application API methods

- Add check_signature method for checking callback signatures

- Deprecate old Verify API methods

# 1.3.0

- Add get_sms_pricing method

- Add get_voice_pricing method

- Add get_event_alert_numbers method to get opt-in/opt-out numbers

- Add resubscribe_event_alert_number method to opt-in a number

- Add more clearly named methods for Verify API

- Add app_name and app_version options

# 1.2.0

- Add topup method

- Add update_settings method

- Add api_host attribute

- Add ClientError and ServerError classes

# 1.1.0

- Move repository to https://github.com/nexmo/nexmo-python

- Add get_basic_number_insight method for Number Insight Basic API

- Add get_number_insight method for Number Insight Standard API

- Add User-Agent header to requests

# 1.0.3

- Change license from LGPL-3.0 to MIT

# 1.0.2

- Remove merge helper function

# 1.0.1

- Python 3.x fixes

# 1.0.0

- First version!
