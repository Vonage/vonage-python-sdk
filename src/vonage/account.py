class Account:
    def __init__(self, client):
        self._client = client

    def get_balance(self):
        return self._client.get(self._client.host(), "/account/get-balance")

    def topup(self, params=None, **kwargs):
        return self._client.post(self._client.host(), "/account/top-up", params or kwargs)

    def get_country_pricing(self, country_code):
        return self._client.get(
            self._client.host(), "/account/get-pricing/outbound", {"country": country_code}
        )

    def get_prefix_pricing(self, prefix):
        return self._client.get(
            self._client.host(), "/account/get-prefix-pricing/outbound", {"prefix": prefix}
        )

    def get_sms_pricing(self, number):
        return self._client.get(
            self._client.host(), "/account/get-phone-pricing/outbound/sms", {"phone": number}
        )

    def get_voice_pricing(self, number):
        return self._client.get(
            self._client.host(), "/account/get-phone-pricing/outbound/voice", {"phone": number}
        )

    def update_default_sms_webhook(self, params=None, **kwargs):
        return self._client.post(self._client.host(), "/account/settings", params or kwargs)

    def list_secrets(self, api_key):
        return self._client.get(
            self._client.api_host(),
            f"/accounts/{api_key}/secrets",
            header_auth=True,
        )

    def get_secret(self, api_key, secret_id):
        return self._client.get(
            self._client.api_host(),
            f"/accounts/{api_key}/secrets/{secret_id}",
            header_auth=True,
        )

    def create_secret(self, api_key, secret):
        body = {"secret": secret}
        return self._client._post_json(
            self._client.api_host(), f"/accounts/{api_key}/secrets", body
        )

    def revoke_secret(self, api_key, secret_id):
        return self._client.delete(
            self._client.api_host(),
            f"/accounts/{api_key}/secrets/{secret_id}",
            header_auth=True,
        )
