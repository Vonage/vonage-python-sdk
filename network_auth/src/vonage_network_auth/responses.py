from typing import Optional

from pydantic import BaseModel


class OidcResponse(BaseModel):
    auth_req_id: str
    expires_in: int
    interval: Optional[int] = None


class TokenResponse(BaseModel):
    access_token: str
    token_type: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
