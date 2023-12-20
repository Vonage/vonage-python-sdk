from pydantic import BaseModel, HttpUrl, AnyUrl, Field, SerializeAsAny
from pydantic.types import  conint, constr, AnyType
from typing import Optional, Dict
from typing_extensions import Literal

class ConnectEndpoints:
    class Endpoint(BaseModel):
        type: str = None

    class PhoneEndpoint(Endpoint):
        type: AnyType = Field('phone', Literal=True)
        number: constr(pattern=r'^[1-9]\d{6,14}$')
        dtmfAnswer: Optional[constr(pattern='^[0-9*#p]+$')] = None
        onAnswer: Optional[Dict[str, HttpUrl]] = None

    class AppEndpoint(Endpoint):
        type: AnyType = Field('app', Literal=True)
        user: str

    class WebsocketEndpoint(Endpoint):
        type: AnyType = Field('websocket', Literal=True)
        uri: AnyUrl
        contentType: Literal['audio/l16;rate=16000', 'audio/l16;rate=8000']
        headers: Optional[dict]

    class SipEndpoint(Endpoint):
        type: AnyType = Field('sip', Literal=True)
        uri: str
        headers: Optional[dict]

    class VbcEndpoint(Endpoint):
        type: AnyType = Field('vbc', Literal=True)
        extension: str

    @classmethod
    def create_endpoint_model_from_dict(cls, d) -> Endpoint:
        if d['type'] == 'phone':
            return cls.PhoneEndpoint.parse_obj(d)
        elif d['type'] == 'app':
            return cls.AppEndpoint.parse_obj(d)
        elif d['type'] == 'websocket':
            return cls.WebsocketEndpoint.parse_obj(d)
        elif d['type'] == 'sip':
            return cls.WebsocketEndpoint.parse_obj(d)
        elif d['type'] == 'vbc':
            return cls.WebsocketEndpoint.parse_obj(d)
        else:
            raise ValueError(
                'Invalid "type" specified for endpoint object. Cannot create a ConnectEndpoints.Endpoint model.'
            )
