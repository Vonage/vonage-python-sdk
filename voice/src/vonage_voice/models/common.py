from typing import Literal, Optional

from pydantic import BaseModel, Field


class AdvancedMachineDetection(BaseModel):
    behavior: Optional[Literal['continue', 'hangup']] = None
    mode: Optional[Literal['default', 'detect', 'detect_beep']] = None
    beep_timeout: Optional[int] = Field(None, ge=45, le=120)
