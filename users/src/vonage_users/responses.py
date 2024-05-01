from typing import List, Optional

from pydantic import BaseModel, Field, model_validator
from vonage_utils.models import Link, ResourceLink


class Links(BaseModel):
    self: Link
    first: Link
    next: Optional[Link] = None
    prev: Optional[Link] = None


class UserSummary(BaseModel):
    id: Optional[str]
    name: Optional[str]
    display_name: Optional[str] = None
    links: Optional[ResourceLink] = Field(None, validation_alias='_links', exclude=True)
    link: Optional[str] = None

    @model_validator(mode='after')
    def get_link(self):
        if self.links is not None:
            self.link = self.links.self.href
        return self


class Embedded(BaseModel):
    users: List[UserSummary] = []


class ListUsersResponse(BaseModel):
    page_size: int
    embedded: Embedded = Field(..., validation_alias='_embedded')
    links: Links = Field(..., validation_alias='_links')
