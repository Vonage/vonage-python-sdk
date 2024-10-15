from typing import Optional

from pydantic import BaseModel, Field, model_validator
from vonage_utils.models import HalLinks, ResourceLink

from .common import ApplicationBase, Keys


class ApplicationData(ApplicationBase):
    """Application object used to structure responses received from the Vonage Application
    API.

    Args:
        name (str): The name of the application.
        capabilities (Capabilities, Optional): The capabilities of the application.
        privacy (Privacy, Optional): The privacy settings for the application.
        keys (Keys, Optional): The application keys.
        id (str): The unique application ID.
        keys (Keys, Optional): The application keys.
        links (ResourceLink, Optional): Links to the application.
        link (str, Optional): The self link of the application.
    """

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
    """Model for embedded application data. This is used in the response model.

    Args:
        applications (list[ApplicationData]): A list of application data objects.
    """

    applications: list[ApplicationData] = []


class ListApplicationsResponse(BaseModel):
    """Response object for listing applications. This is used when providing lists of the
    applications associated with a Vonage account.

    Args:
        page_size (int, Optional): The number of applications to return per page.
        page (int): The page number to return.
        total_items (int, Optional): The total number of applications.
        total_pages (int, Optional): The total number of pages.
        embedded (Embedded): Embedded application data.
        links (HalLinks): Links to the pages, used for pagination/cursoring.
    """

    page_size: Optional[int] = None
    page: int = Field(None, ge=1)
    total_items: Optional[int] = None
    total_pages: Optional[int] = None
    embedded: Embedded = Field(..., validation_alias='_embedded')
    links: HalLinks = Field(..., validation_alias='_links')
