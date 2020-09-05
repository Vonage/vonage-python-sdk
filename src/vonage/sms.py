import vonage, pytz
from datetime import datetime
from ._internal import _format_date_param

class Sms:
    #To init Sms class pass a client reference or a key and secret
    def __init__(
        self,
        client=None,
        key=None,
        secret=None,
        signature_secret=None,
        signature_method=None
    ):
        try:
            self._client = client
            if self._client is None:
                self._client = vonage.Client(
                    key=key,
                    secret=secret,
                    signature_secret=signature_secret,
                    signature_method=signature_method
                )
        except Exception as e:
            print('Error: {error_message}'.format(error_message=str(e)))
    
    def send_message(self, params):
        """
        Send an SMS message.
        Requires a client initialized with `key` and either `secret` or `signature_secret`.
        :param dict params: A dict of values described at `Send an SMS <https://developer.nexmo.com/api/sms#send-an-sms>`_
        """
        return self._client.post(self._client.host(), "/sms/json", params, supports_signature_auth=True)
    
    def submit_sms_conversion(self, message_id, delivered=True, timestamp=None):
        """
        Notify Nexmo that an SMS was successfully received.

        :param message_id: The `message-id` str returned by the send_message call.
        :param delivered: A `bool` indicating that the message was or was not successfully delivered.
        :param timestamp: A `datetime` object containing the time the SMS arrived.
        :return: The parsed response from the server. On success, the bytestring b'OK'
        """
        params = {
            "message-id": message_id,
            "delivered": delivered,
            "timestamp": timestamp or datetime.now(pytz.utc)
        }
        # Ensure timestamp is a string:
        _format_date_param(params, "timestamp")
        return self._client.post(self._client.api_host(), "/conversions/sms", params)
