from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from vonage import Client


class NumberInsightV2:
    def __init__(self, client: Client):
        self._client = client
        self._auth_type = 'header'

    def fraud_check(self, params: dict):
        return self._client.post(
            self._client.api_host(), '/v2/ni', params, auth_type=self._auth_type
        )
