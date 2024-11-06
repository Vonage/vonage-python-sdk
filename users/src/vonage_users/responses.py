from typing import Optional

from pydantic import BaseModel, Field, model_validator
from vonage_utils.models import Link, ResourceLink


class Links(BaseModel):
    """Model for links following a version of the HAL standard.

    Args:
        self (Link): The self link.
        first (Link): The first link.
        next (Link, Optional): The next link.
        prev (Link, Optional): The previous link.
    """

    self: Link
    first: Link
    next: Optional[Link] = None
    prev: Optional[Link] = None


class UserSummary(BaseModel):
    """Model for a user summary - a subset of user information.

    Args:
        id (str, Optional): The user ID.
        name (str, Optional): The name of the user.
        display_name (str, Optional): The display name of the user.
        links (ResourceLink, Optional): Links to the user resource.
        link (str, Optional): The `_self` link.
    """

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
    """Model for embedded resources.

    Args:
        users (list[UserSummary]): A list of user summaries.
    """

    users: list[UserSummary] = []


class ListUsersResponse(BaseModel):
    """Model for a response containing a list of users.

    Args:
        page_size (int): The number of users returned in the response.
        embedded (Embedded): Embedded resources.
        links (Links): Links to other pages of users.
    """

    page_size: int
    embedded: Embedded = Field(..., validation_alias='_embedded')
    links: Links = Field(..., validation_alias='_links')
