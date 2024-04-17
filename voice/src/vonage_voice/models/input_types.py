from typing import List, Optional

from pydantic import BaseModel, Field


class Dtmf(BaseModel):
    timeOut: Optional[int] = Field(None, ge=0, le=10)
    maxDigits: Optional[int] = Field(None, ge=1, le=20)
    submitOnHash: Optional[bool] = None


class Speech(BaseModel):
    uuid: Optional[List[str]] = None
    endOnSilence: Optional[float] = Field(None, ge=0.4, le=10.0)
    language: Optional[str] = None
    context: Optional[List[str]] = None
    startTimeout: Optional[int] = Field(None, ge=1, le=60)
    maxDuration: Optional[int] = Field(None, ge=1, le=60)
    saveAudio: Optional[bool] = False
    sensitivity: Optional[int] = Field(None, ge=0, le=100)
