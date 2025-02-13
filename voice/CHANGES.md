# 1.3.0
- Add new `headers` and `standard_headers` options to the `Sip` data model
- Add new `standardHeaders` option to the `SipEndpoint` NCCO model
- Add check for invalid hostnames when downloading a recording with `Voice.download_recording`
- Allow the `CreateCallRequest` model to accept a SIP URI as well as a phone number in the `from_` field

# 1.2.0
- Make all models originally accessed by `vonage_voice.models.***` available at the top level of the package, i.e. `vonage_voice.***`

# 1.1.2
- Update incorrect return type annotation for `Voice.download_recording`

# 1.1.1
- Remove maximum webhook uri length constraint

# 1.1.0
- Add `Voice.get_recording` method to get call recordings
- Add `Voice.verify_signature` method to expose the verification functionality from `vonage-jwt`
- Updated dependency versions

# 1.0.6
- Update dependency versions

# 1.0.5
- Support for Python 3.13, drop support for 3.8

# 1.0.4
- Add docstrings to data models

# 1.0.3
- Internal refactoring

# 1.0.2
- Update minimum dependency version

# 1.0.1
- Initial upload

# 1.0.0
- This version was skipped due to a technical issue with the package distribution. Please use version 1.0.1 or later.