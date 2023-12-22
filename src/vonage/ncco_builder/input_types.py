from pydantic import BaseModel, confloat, conint
from typing import List


class InputTypes:
    class Dtmf(BaseModel):
        timeOut: conint(ge=0, le=10) = None
        maxDigits: conint(ge=1, le=20) = None
        submitOnHash: bool = None

    class Speech(BaseModel):
        uuid: str = None
        endOnSilence: confloat(ge=0.4, le=10.0) = None
        language: str = None
        context: List[str] = None
        startTimeout: conint(ge=1, le=60) = None
        maxDuration: conint(ge=1, le=60) = None
        saveAudio: bool = None

    @classmethod
    def create_dtmf_model(cls, dict) -> Dtmf:
        return cls.Dtmf.model_validate(dict)

    @classmethod
    def create_speech_model(cls, dict) -> Speech:
        return cls.Speech.model_validate(dict)
