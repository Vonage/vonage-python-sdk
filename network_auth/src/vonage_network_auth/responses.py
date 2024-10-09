from typing import Optional

from pydantic import BaseModel


class OidcResponse(BaseModel):
    """Model for an OpenID Connect response.

    Args:
        auth_req_id (str): The authentication request ID.
        expires_in (int): The time in seconds until the authentication code expires.
        interval (int, Optional): The time in seconds until the next request can be made.
    """

    auth_req_id: str
    expires_in: int
    interval: Optional[int] = None


class TokenResponse(BaseModel):
    """Model for a token response.

    Args:
        access_token (str): The access token.
        token_type (str, Optional): The token type.
        refresh_token (str, Optional): The refresh token.
        expires_in (int, Optional): The time until the token expires.
    """

    access_token: str
    token_type: Optional[str] = None
    refresh_token: Optional[str] = None
    expires_in: Optional[int] = None
