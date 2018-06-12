# 2.1.0
* Added support for `get_recording`
* Added support for SMS conversion
* Added debug logging for most calls, under the 'nexmo' logger.
* Internal refactoring (affects only private methods.)

# 2.0.0
* Drop support for Python 3.3 (in line with the cryptography library we depend upon)
* Ensure timestamp is added the params list if signing requests
* Avoid value injection in signature auth.
* Add support for different hashes for signature generation (thanks @trancee!)
* Tests ported to pytest

# 1.5.0

* Added ability to provide a file path as private_key param no the nexmo.Client constructor

* Added send/stop endpoints for audio/speech/dtmf

* Added new number insight endpoints

# 1.4.0

* Added new Voice API call methods

* Added Application API methods

* Added check_signature method for checking callback signatures

* Deprecated old Verify API methods

# 1.3.0

* Added get_sms_pricing method

* Added get_voice_pricing method

* Added get_event_alert_numbers method to get opt-in/opt-out numbers

* Added resubscribe_event_alert_number method to opt-in a number

* Added more clearly named methods for Verify API

* Added app_name and app_version options

# 1.2.0

* Added topup method

* Added update_settings method

* Added api_host attribute

* Added ClientError and ServerError classes

# 1.1.0

* Moved repository to https://github.com/Nexmo/nexmo-python

* Added get_basic_number_insight method for Number Insight Basic API

* Added get_number_insight method for Number Insight Standard API

* Added User-Agent header to requests

# 1.0.3

* Changed license from LGPL-3.0 to MIT

# 1.0.2

* Removed merge helper function

# 1.0.1

* Python 3.x fixes

# 1.0.0

* First version!
