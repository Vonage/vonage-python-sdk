from typing import Literal, Optional, Union

from pydantic import BaseModel


class BasicInsightResponse(BaseModel):
    status: int = None
    status_message: str = None
    request_id: Optional[str] = None
    international_format_number: Optional[str] = None
    national_format_number: Optional[str] = None
    country_code: Optional[str] = None
    country_code_iso3: Optional[str] = None
    country_name: Optional[str] = None
    country_prefix: Optional[str] = None


class Carrier(BaseModel):
    network_code: Optional[str] = None
    name: Optional[str] = None
    country: Optional[str] = None
    network_type: Optional[str] = None


class CallerIdentity(BaseModel):
    caller_type: Optional[str] = None
    caller_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    subscription_type: Optional[str] = None


class StandardInsightResponse(BasicInsightResponse):
    request_price: Optional[str] = None
    refund_price: Optional[str] = None
    remaining_balance: Optional[str] = None
    current_carrier: Optional[Carrier] = None
    original_carrier: Optional[Carrier] = None
    ported: Optional[str] = None
    caller_identity: Optional[CallerIdentity] = None


class RoamingStatus(BaseModel):
    status: Optional[str] = None
    roaming_country_code: Optional[str] = None
    roaming_network_code: Optional[str] = None
    roaming_network_name: Optional[str] = None


class RealTimeData(BaseModel):
    active_status: Optional[str] = None
    handset_status: Optional[str] = None


class AdvancedSyncInsightResponse(StandardInsightResponse):
    roaming: Optional[Union[RoamingStatus, Literal['unknown']]] = None
    lookup_outcome: Optional[int] = None
    lookup_outcome_message: Optional[str] = None
    valid_number: Optional[str] = None
    reachable: Optional[str] = None
    real_time_data: Optional[RealTimeData] = None


class AdvancedAsyncInsightResponse(BaseModel):
    request_id: Optional[str] = None
    number: Optional[str] = None
    remaining_balance: Optional[str] = None
    request_price: Optional[str] = None
    status: Optional[int] = None
    error_text: Optional[str] = None
