from requests import Response
from vonage_utils.errors import VonageError


class SmsError(VonageError):
    """Indicates an error with the Vonage SMS Package."""


class PartialFailureError(SmsError):
    """Indicates that a request was partially successful."""

    def __init__(self, response: Response):
        self.message = (
            'Sms.send_message method partially failed. Not all of the message(s) sent successfully.',
        )
        super().__init__(self.message)
        self.response = response


class SmsThrottleError(SmsError):
    """Indicates that the SMS requests are being throttled due to too many requests in a short period."""
