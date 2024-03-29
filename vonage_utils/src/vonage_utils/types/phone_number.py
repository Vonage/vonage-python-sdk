from typing import Annotated

from pydantic import Field

PhoneNumber = Annotated[str, Field(pattern=r'^[1-9]\d{6,14}$')]
