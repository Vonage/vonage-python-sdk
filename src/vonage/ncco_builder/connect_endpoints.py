from pydantic import BaseModel, HttpUrl, AnyUrl, constr, field_serializer, Field
from typing import Dict
from typing_extensions import Annotated, Literal


class ConnectEndpoints:
    class Endpoint(BaseModel):
        type: Literal['phone', 'app', 'websocket', 'sip', 'vbc'] = None

    class PhoneEndpoint(Endpoint):
        type: Literal['phone'] = 'phone'

        number: constr(pattern=r'^[1-9]\d{6,14}$')
        dtmfAnswer: constr(pattern='^[0-9*#p]+$') = None
        onAnswer: Dict[str, HttpUrl] = None

        @field_serializer('onAnswer')
        def serialize_dt(self, oa: Dict[str, HttpUrl], _info):
            if oa is None:
                return oa

            return {k: str(v) for k, v in oa.items()}

    class AppEndpoint(Endpoint):
        type: Literal['app'] = 'app'
        user: str

    class WebsocketEndpoint(Endpoint):
        type: Literal['websocket'] = 'websocket'

        uri: AnyUrl
        contentType: Annotated[
            Literal['audio/l16;rate=16000', 'audio/l16;rate=8000'],
            Field(serialization_alias='content-type'),
        ]
        headers: dict = None

        @field_serializer('uri')
        def serialize_uri(self, uri: AnyUrl, _info):
            return str(uri)

    class SipEndpoint(Endpoint):
        type: Literal['sip'] = 'sip'
        uri: str
        headers: dict = None

    class VbcEndpoint(Endpoint):
        type: Literal['vbc'] = 'vbc'
        extension: str

    @classmethod
    def create_endpoint_model_from_dict(cls, d) -> Endpoint:
        if d['type'] == 'phone':
            return cls.PhoneEndpoint.model_validate(d)
        elif d['type'] == 'app':
            return cls.AppEndpoint.model_validate(d)
        elif d['type'] == 'websocket':
            return cls.WebsocketEndpoint.model_validate(d)
        elif d['type'] == 'sip':
            return cls.WebsocketEndpoint.model_validate(d)
        elif d['type'] == 'vbc':
            return cls.WebsocketEndpoint.model_validate(d)
        else:
            raise ValueError(
                'Invalid "type" specified for endpoint object. Cannot create a ConnectEndpoints.Endpoint model.'
            )
