from vonage_utils.errors import VonageError


class VerifyError(VonageError):
    """Indicates an error with the Vonage Verify Package."""


# class PartialFailureError(SmsError):
#     """Indicates that a request was partially successful."""

#     def __init__(self, response: Response):
#         self.message = (
#             'Sms.send_message method partially failed. Not all of the message(s) sent successfully.',
#         )
#         super().__init__(self.message)
#         self.response = response
