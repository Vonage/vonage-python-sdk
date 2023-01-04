from pydantic import BaseModel, AnyUrl, Field, validator, constr, confloat, conint
from typing import Optional, Union, List
from typing_extensions import Literal


class InputTypes:
    class Dtmf(BaseModel):
        timeOut: Optional[conint(le=0, ge=10)]
        maxDigits: Optional[conint(le=1, ge=20)]
        submitOnHash: Optional[bool]

    class Speech(BaseModel):
        ...

    @classmethod
    def create_dtmf_model(cls, dict):
        return cls.Dtmf.parse_obj(dict)

    @classmethod
    def create_speech_model(cls, dict):
        return cls.Speech.parse_obj(dict)
