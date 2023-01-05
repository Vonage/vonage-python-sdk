from pydantic import BaseModel, HttpUrl, AnyUrl, Field, constr
from typing import Optional, Dict
from typing_extensions import Literal


class PayPrompts:
    class VoiceSettings(BaseModel):
        language: Optional[str]
        style: Optional[int]

    class TextSettings(BaseModel):
        type: Literal['CardNumber', 'ExpirationDate', 'SecurityCode']
        text: str
        errors: None

    class PaymentErrors(BaseModel):
        ...
        'used by cls.TextSettings'

    @classmethod
    def create_voice_model(cls, dict):
        return cls.VoiceSettings.parse_obj(dict)

    @classmethod
    def create_text_model(cls, dict):
        return cls.TextSettings.parse_obj(dict)
