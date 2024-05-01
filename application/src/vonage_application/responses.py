from typing import Optional

from pydantic import BaseModel, Field, model_validator
from vonage_utils.models import ResourceLink

from .common import ApplicationBase

# class Embedded(BaseModel):
#     users: List[UserSummary] = []


# class ListApplicationsResponse(BaseModel):
#     page_size: int
#     embedded: Embedded = Field(..., validation_alias='_embedded')
#     links: Links = Field(..., validation_alias='_links')


class KeysResponse(BaseModel):
    public_key: Optional[str] = None
    private_key: Optional[str] = None


class ApplicationData(ApplicationBase):
    id: str
    keys: Optional[KeysResponse] = None
    links: Optional[ResourceLink] = Field(None, validation_alias='_links', exclude=True)
    link: Optional[str] = None

    @model_validator(mode='after')
    def get_link(self):
        if self.links is not None:
            self.link = self.links.self.href
        return self
