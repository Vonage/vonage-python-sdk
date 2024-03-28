from typing import List, Optional

from pydantic import BaseModel, Field, model_validator
from vonage_users.common import Link, ResourceLink


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
    @classmethod
    def get_link(cls, data):
        if data.links is not None:
            data.link = data.links.self.href
        return data


class Embedded(BaseModel):
    users: List[UserSummary] = []


class ListUsersResponse(BaseModel):
    page_size: int
    embedded: Embedded = Field(..., validation_alias='_embedded')
    links: Links = Field(..., validation_alias='_links')
