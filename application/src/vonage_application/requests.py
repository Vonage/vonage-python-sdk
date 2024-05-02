from typing import Optional

from pydantic import BaseModel

from .common import ApplicationBase


class ListApplicationsFilter(BaseModel):
    """Request object for filtering applications."""

    page_size: Optional[int] = 100
    page: int = None


class ApplicationConfig(ApplicationBase):
    pass
