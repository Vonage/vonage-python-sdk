from typing import Optional

from pydantic import BaseModel, Field


class Balance(BaseModel):
    value: float
    auto_reload: Optional[bool] = Field(None, validation_alias='autoReload')
