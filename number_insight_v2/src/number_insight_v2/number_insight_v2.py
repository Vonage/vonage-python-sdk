from copy import deepcopy
from dataclasses import dataclass
from typing import List, Union

from pydantic import BaseModel

from http_client.http_client import HttpClient


class FraudCheckRequest(BaseModel):
    """"""

    number: str
    insights: Union[str, List[str]]


@dataclass
class FraudCheckResponse:
    ...


#     phone: Phone
#     sim: SimSwap


class NumberInsightv2:
    """Number Insight API V2."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = deepcopy(http_client)
        self._http_client._parse_response = self.response_parser
        self._auth_type = 'header'

    def fraud_check(self, number: str, insights: Union[str, List[str]]):
        """"""

    def fraud_check(self, request: FraudCheckRequest) -> FraudCheckResponse:
        """"""
        response = self._http_client.post('/ni/fraud', request.model_dump())
        return FraudCheckResponse(response)

    def response_parser(self, response):
        """"""
