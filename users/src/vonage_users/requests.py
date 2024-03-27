from typing import Literal, Optional

from pydantic import BaseModel, Field


class ListUsersRequest(BaseModel):
    """Request object for listing users."""

    page_size: Optional[int] = Field(2, ge=1, le=100)
    order: Optional[Literal['asc', 'desc', 'ASC', 'DESC']] = None
    cursor: Optional[str] = Field(
        None,
        description="The cursor to start returning results from. You are not expected to provide this manually, but to follow the url provided in _links.next.href or _links.prev.href in the response which contains a cursor value.",
    )
    name: Optional[str] = None
