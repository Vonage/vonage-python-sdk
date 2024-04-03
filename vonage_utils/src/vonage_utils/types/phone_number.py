from pydantic import Field
from typing_extensions import Annotated

PhoneNumber = Annotated[str, Field(pattern=r'^[1-9]\d{6,14}$')]
