from typing import List, Optional

from pydantic import BaseModel, Field, model_validator
from vonage_utils.models import HalLinks, ResourceLink

from .common import ApplicationBase, Keys


class ApplicationData(ApplicationBase):
    id: str
    keys: Optional[Keys] = None
    links: Optional[ResourceLink] = Field(None, validation_alias='_links', exclude=True)
    link: Optional[str] = None

    @model_validator(mode='after')
    def get_link(self):
        if self.links is not None:
            self.link = self.links.self.href
        return self


class Embedded(BaseModel):
    applications: List[ApplicationData] = []


class ListApplicationsResponse(BaseModel):
    page_size: Optional[int] = None
    page: int = Field(None, ge=1)
    total_items: Optional[int] = None
    total_pages: Optional[int] = None
    embedded: Embedded = Field(..., validation_alias='_embedded')
    links: HalLinks = Field(..., validation_alias='_links')
