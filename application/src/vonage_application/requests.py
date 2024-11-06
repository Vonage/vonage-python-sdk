from typing import Optional

from pydantic import BaseModel

from .common import ApplicationBase


class ListApplicationsFilter(BaseModel):
    """Request object for filtering applications.

    Args:
        page_size (int, Optional): The number of applications to return per page.
        page (int, Optional): The page number to return.
    """

    page_size: Optional[int] = 100
    page: int = None


class ApplicationConfig(ApplicationBase):
    """Application object used in requests when communicating with the Vonage Application
    API.

    Args:
        name (str): The name of the application.
        capabilities (Capabilities, Optional): The capabilities of the application.
        privacy (Privacy, Optional): The privacy settings for the application.
        keys (Keys, Optional): The application keys.
    """
