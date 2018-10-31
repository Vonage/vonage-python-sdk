# 2.3.0
* Explicit parameter list for the `nexmo.Client` constructor. **This may cause errors in code passing incorrect or spurious arguments to the Client constructor.**
* Secret Management
* Support for Authorization header authentication.

# 2.2.0
* Add support for `redact_transaction`.

# 2.1.0
* Add support for `get_recording`
* Add support for SMS conversion
* Add debug logging for most calls, under the 'nexmo' logger.
* Internal refactoring (affects only private methods.)

# 2.0.0
* Drop support for Python 3.3 (in line with the cryptography library we depend upon)
* Ensure timestamp is added the params list if signing requests
* Avoid value injection in signature auth.
* Add support for different hashes for signature generation (thanks @trancee!)
* Tests ported to pytest

# 1.5.0

* Add ability to provide a file path as private_key param no the nexmo.Client constructor

* Add send/stop endpoints for audio/speech/dtmf

* Add new number insight endpoints

# 1.4.0

* Add new Voice API call methods

* Add Application API methods

* Add check_signature method for checking callback signatures

* Deprecate old Verify API methods

# 1.3.0

* Add get_sms_pricing method

* Add get_voice_pricing method

* Add get_event_alert_numbers method to get opt-in/opt-out numbers

* Add resubscribe_event_alert_number method to opt-in a number

* Add more clearly named methods for Verify API

* Add app_name and app_version options

# 1.2.0

* Add topup method

* Add update_settings method

* Add api_host attribute

* Add ClientError and ServerError classes

# 1.1.0

* Move repository to https://github.com/Nexmo/nexmo-python

* Add get_basic_number_insight method for Number Insight Basic API

* Add get_number_insight method for Number Insight Standard API

* Add User-Agent header to requests

# 1.0.3

* Change license from LGPL-3.0 to MIT

# 1.0.2

* Remove merge helper function

# 1.0.1

* Python 3.x fixes

# 1.0.0

* First version!
