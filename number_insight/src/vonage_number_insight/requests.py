from typing import Optional

from pydantic import BaseModel
from vonage_utils.types import PhoneNumber


class BasicInsightRequest(BaseModel):
    number: PhoneNumber
    country: Optional[str] = None


class StandardInsightRequest(BasicInsightRequest):
    cnam: Optional[bool] = None


class AdvancedAsyncInsightRequest(StandardInsightRequest):
    callback: str


class AdvancedSyncInsightRequest(StandardInsightRequest):
    real_time_data: Optional[bool] = None
