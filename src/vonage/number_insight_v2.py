from __future__ import annotations
from typing import TYPE_CHECKING, Union

from .errors import NumberInsightV2Error
from ._internal import validate_phone_number

if TYPE_CHECKING:
    from vonage import Client


class NumberInsightV2:
    def __init__(self, client: Client):
        self._client = client
        self._auth_type = 'header'

    def fraud_check(self, number: str, insights: Union[str, list]):
        validate_phone_number(number)
        params = {'type': 'phone', 'phone': number}

        if type(insights) == str:
            insights_list = [insights]
        elif type(insights) == list:
            insights_list = insights
        else:
            raise NumberInsightV2Error(
                'You must pass in values for the "insights" parameter as a string or a list.'
            )

        for insight in insights_list:
            self._validate_insight(insight)
        params['insights'] = insights_list

        return self._client.post(
            self._client.api_host(), '/v2/ni', params, auth_type=self._auth_type
        )

    def _validate_insight(self, insight: str):
        if insight not in ('fraud_score', 'sim_swap'):
            raise NumberInsightV2Error(
                f'The only insights that can be requested are "fraud_score" and "sim_swap. You requested: "{insight}".'
            )
