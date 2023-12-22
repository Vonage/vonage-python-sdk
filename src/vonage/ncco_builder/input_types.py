from pydantic import BaseModel, confloat, conint
from typing import Optional, List


class InputTypes:
    class Dtmf(BaseModel):
        timeOut: Optional[conint(ge=0, le=10)] = None
        maxDigits: Optional[conint(ge=1, le=20)] = None
        submitOnHash: Optional[bool] = None

    class Speech(BaseModel):
        uuid: Optional[str] = None
        endOnSilence: Optional[confloat(ge=0.4, le=10.0)] = None
        language: Optional[str] = None
        context: Optional[List[str]] = None
        startTimeout: Optional[conint(ge=1, le=60)] = None
        maxDuration: Optional[conint(ge=1, le=60)] = None
        saveAudio: Optional[bool] = None

    @classmethod
    def create_dtmf_model(cls, dict) -> Dtmf:
        return cls.Dtmf.model_validate(dict)

    @classmethod
    def create_speech_model(cls, dict) -> Speech:
        return cls.Speech.model_validate(dict)
