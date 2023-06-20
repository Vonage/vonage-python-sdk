from __future__ import annotations
from typing import TYPE_CHECKING
from typing import Union, Literal

if TYPE_CHECKING:
    from vonage import Client


class NumberInsightV2:
    def __init__(self, client: Client):
        self._client = client
        self._auth_type = 'header'

    def fraud_check(self, number: str, insights: Union[str, list]):
        params = {'type': 'phone', 'phone': number}

        if type(insights) == str:
            if insights == 'fraud_score' or insights == 'sim_swap':
                params['insights'] = [insights]
        elif type(insights) == 'list':
            # need to add validation to this particular section
            params['insights'] == insights
        print(params)
        return self._client.post(
            self._client.api_host(), '/v2/ni', params, auth_type=self._auth_type
        )
