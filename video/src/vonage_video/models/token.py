from time import time
from typing import List, Literal, Optional, Union
from uuid import UUID, uuid4

from pydantic import BaseModel, field_validator, model_validator

from ..errors import TokenExpiryError
from .enums import TokenRole


class TokenOptions(BaseModel):
    """Options for generating a token for the Vonage Video API.

    Args:
    - session_id (str): The session ID.
    - role (TokenRole): The role of the token. Defaults to 'publisher'.
    - connection_data (str): The connection data for the token.
    - initial_layout_class_list (List[str]): The initial layout class list for the token.
    - exp (int): The expiry date for the token. Defaults to 15 minutes from the current time.
    - jti (Union[UUID, str]): The JWT ID for the token. Defaults to a new UUID.
    - iat (float): The time the token was issued. Defaults to the current time.
    - subject (str): The subject of the token. Defaults to 'video'.
    - scope (str): The scope of the token. Defaults to 'session.connect'.
    - acl (dict): The access control list for the token. NOTE: Do not change this value.
    """

    session_id: str
    role: Optional[TokenRole] = TokenRole.PUBLISHER
    connection_data: Optional[str] = None
    initial_layout_class_list: Optional[List[str]] = None
    exp: Optional[int] = None
    jti: Union[UUID, str] = uuid4()
    iat: int = int(time())
    subject: Literal['video'] = 'video'
    scope: Literal['session.connect'] = 'session.connect'
    acl: dict = {'paths': {'/session/**': {}}}

    @field_validator('exp')
    @classmethod
    def validate_exp(cls, v: int):
        now = int(time())
        if v < now:
            raise TokenExpiryError('Token expiry date must be in the future.')
        if v > now + 3600 * 24 * 30:
            raise TokenExpiryError(
                'Token expiry date must be less than 30 days from now.'
            )
        return v

    @model_validator(mode='after')
    def set_exp(self):
        if self.exp is None:
            self.exp = self.iat + 15 * 60
        return self

    @model_validator(mode='after')
    def enforce_acl_default_value(self):
        self.acl = {'paths': {'/session/**': {}}}
        return self
