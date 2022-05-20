import vonage

def send_message(message):
    return self._client.post(self._client.host(), "/sms/json", params, supports_signature_auth=True)


