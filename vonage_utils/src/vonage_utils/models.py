from pydantic import BaseModel


class Link(BaseModel):
    href: str


class ResourceLink(BaseModel):
    self: Link
