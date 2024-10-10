from typing import Literal, Optional

from pydantic import BaseModel, Field


class ListUsersFilter(BaseModel):
    """Request object for listing users.

    Args:
        page_size (int, Optional): The number of users to return per response.
        order (str, Optional): Return the records in ascending or descending order.
        cursor (str, Optional): The cursor to start returning results from. You must
            follow the url provided in the response tuple which contains a cursor value.
        name (str, Optional): The name of the user to filter by.
    """

    page_size: Optional[int] = Field(100, ge=1, le=100)
    order: Optional[Literal['asc', 'desc', 'ASC', 'DESC']] = None
    cursor: Optional[str] = Field(
        None,
        description="The cursor to start returning results from. You are not expected to provide this manually, but to follow the url provided in _links.next.href or _links.prev.href in the response which contains a cursor value.",
    )
    name: Optional[str] = None
