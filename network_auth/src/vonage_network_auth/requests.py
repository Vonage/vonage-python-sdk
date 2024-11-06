from typing import Optional

from pydantic import BaseModel


class CreateOidcUrl(BaseModel):
    """Model to craft a URL for OIDC authentication.

    Args:
        redirect_uri (str): The URI to redirect to after authentication.
        state (str): A unique identifier for the request. Can be any string.
        login_hint (str): The phone number to use for the request.
    """

    redirect_uri: str
    state: str
    login_hint: str
    scope: Optional[
        str
    ] = 'openid dpv:FraudPreventionAndDetection#number-verification-verify-read'
