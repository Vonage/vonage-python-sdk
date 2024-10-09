from typing import Optional

from pydantic import BaseModel


class Link(BaseModel):
    """Model for a link object.

    Args:
        href (str): The URL of the link.
    """

    href: str


class ResourceLink(BaseModel):
    """Model for a resource link object.

    Args:
        self (Link): The self link of the resource.
    """

    self: Link


class HalLinks(BaseModel):
    """Model for links following a version of the HAL standard.

    Args:
        self (Link): The self link.
        first (Link, Optional): The first link.
        last (Link, Optional): The last link.
        prev (Link, Optional): The previous link.
        next (Link, Optional): The next link.
    """

    self: Link
    first: Optional[Link] = None
    last: Optional[Link] = None
    prev: Optional[Link] = None
    next: Optional[Link] = None
