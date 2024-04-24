from typing import Optional

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


class StandardInsightResponse(BasicInsightResponse):
    ...


class AdvancedAsyncInsightResponse(BaseModel):
    ...


class AdvancedSyncInsightResponse(BaseModel):
    ...
