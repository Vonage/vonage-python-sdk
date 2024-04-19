from pydantic import BaseModel


class Link(BaseModel):
    href: str
