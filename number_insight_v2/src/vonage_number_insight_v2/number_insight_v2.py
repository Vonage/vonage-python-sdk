from copy import deepcopy
from dataclasses import dataclass
from typing import List, Literal, Optional, Union

from pydantic import BaseModel, field_validator, validate_call
from vonage_http_client.http_client import HttpClient

from vonage_utils import format_phone_number


class FraudCheckRequest(BaseModel):
    phone: Union[str, int]
    insights: Union[
        Literal['fraud_score', 'sim_swap'], List[Literal['fraud_score', 'sim_swap']]
    ] = ['fraud_score', 'sim_swap']
    type: Literal['phone'] = 'phone'

    @field_validator('phone')
    @classmethod
    def format_phone_number(cls, value):
        return format_phone_number(value)


@dataclass
class Phone:
    phone: str
    carrier: Optional[str] = None
    type: Optional[str] = None


@dataclass
class FraudScore:
    risk_score: str
    risk_recommendation: str
    label: str
    status: str


@dataclass
class SimSwap:
    status: str
    swapped: Optional[bool] = None
    reason: Optional[str] = None


@dataclass
class FraudCheckResponse:
    request_id: str
    type: str
    phone: Phone
    fraud_score: Optional[FraudScore]
    sim_swap: Optional[SimSwap]


class NumberInsightV2:
    """Number Insight API V2."""

    def __init__(self, http_client: HttpClient) -> None:
        self._http_client = deepcopy(http_client)
        self._auth_type = 'basic'

    @validate_call
    def fraud_check(self, request: FraudCheckRequest) -> FraudCheckResponse:
        """Initiate a fraud check request."""
        response = self._http_client.post(
            self._http_client.api_host,
            '/v2/ni',
            request.model_dump(),
            self._auth_type,
        )

        phone = Phone(**response['phone'])
        fraud_score = (
            FraudScore(**response['fraud_score']) if 'fraud_score' in response else None
        )
        sim_swap = SimSwap(**response['sim_swap']) if 'sim_swap' in response else None

        return FraudCheckResponse(
            request_id=response['request_id'],
            type=response['type'],
            phone=phone,
            fraud_score=fraud_score,
            sim_swap=sim_swap,
        )
