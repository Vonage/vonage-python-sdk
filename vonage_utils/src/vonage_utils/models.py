from typing import Optional

from pydantic import BaseModel


class Link(BaseModel):
    href: str


class ResourceLink(BaseModel):
    self: Link


class HalLinks(BaseModel):
    self: Link
    first: Optional[Link] = None
    last: Optional[Link] = None
    prev: Optional[Link] = None
    next: Optional[Link] = None
