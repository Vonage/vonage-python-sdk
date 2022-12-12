import pytz
from datetime import datetime
from ._internal import _format_date_param
from .errors import SmsError, PartialFailureError

class Sms:
    defaults = {'auth_type': 'params', 'body_is_json': False}

    def __init__(self, client):
        self._client = client
    
    def send_message(self, params):
        """
        Send an SMS message.
        Requires a client initialized with `key` and either `secret` or `signature_secret`.
        :param dict params: A dict of values described at `Send an SMS <https://developer.vonage.com/api/sms#send-an-sms>`_
        """
        response_data = self._client.post(
            self._client.host(), 
            "/sms/json", 
            params, 
            supports_signature_auth=True,
            **Sms.defaults,
        )

        if int(response_data['message-count']) > 1:
            self.check_for_partial_failure(response_data)
        else:
            self.check_for_failure(response_data)

        return response_data

    def check_for_partial_failure(self, response_data):
        successful_messages = 0
        total_messages = int(response_data['message-count'])
        
        for message in response_data['messages']:
            if message['status'] == '0':
                successful_messages += 1
        if successful_messages < total_messages: 
            raise PartialFailureError('Sms.send_message method partially failed. Not all of the message sent successfully.')

    def check_for_failure(self, response_data):
        if int(response_data['messages'][0]['status']) != 0:
                raise SmsError(f'Sms.send_message method failed with error code {response_data["messages"][0]["status"]}: {response_data["messages"][0]["error-text"]}')
    
    def submit_sms_conversion(self, message_id, delivered=True, timestamp=None):
        """
        Notify Vonage that an SMS was successfully received.

        If you are using the Verify API for 2FA, this information is sent to Vonage automatically
        so you do not need to use this method to submit conversion data about 2FA messages.

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
        return self._client.post(self._client.api_host(), "/conversions/sms", params, **Sms.defaults)
