from typing import Optional

from pydantic import BaseModel

from .common import ApplicationBase


class ListApplicationsFilter(BaseModel):
    """Request object for listing users."""

    page_size: Optional[int] = 100
    page: int = None


class KeysRequest(BaseModel):
    public_key: str


class ApplicationOptions(ApplicationBase):
    keys: Optional[KeysRequest] = None
