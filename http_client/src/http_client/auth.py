from base64 import b64encode
from typing import Optional

from pydantic import validate_call
from vonage_jwt.jwt import JwtClient

from .errors import InvalidAuthError, JWTGenerationError


class Auth:
    """Deals with Vonage API authentication.

    Args:
    - api_key (str): The API key for authentication.
    - api_secret (str): The API secret for authentication.
    - application_id (str): The application ID for JWT authentication.
    - private_key (str): The private key for JWT authentication.

    Note:
    To use JWT authentication, provide values for both `application_id` and `private_key`.
    """

    @validate_call
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        application_id: Optional[str] = None,
        private_key: Optional[str] = None,
    ) -> None:
        self._validate_input_combinations(
            api_key, api_secret, application_id, private_key
        )

        self._api_key = api_key
        self._api_secret = api_secret

        if application_id is not None and private_key is not None:
            self._jwt_client = JwtClient(application_id, private_key)

    @property
    def api_key(self):
        return self._api_key

    @property
    def api_secret(self):
        return self._api_secret

    def create_jwt_auth_string(self):
        return b'Bearer ' + self.generate_application_jwt()

    def generate_application_jwt(self):
        try:
            return self._jwt_client.generate_application_jwt()
        except AttributeError as err:
            raise JWTGenerationError(
                'JWT generation failed. Check that you passed in valid values for "application_id" and "private_key".'
            ) from err

    def create_basic_auth_string(self):
        hash = b64encode(f'{self.api_key}:{self.api_secret}'.encode('utf-8')).decode(
            'ascii'
        )
        return f'Basic {hash}'

    def _validate_input_combinations(
        self, api_key, api_secret, application_id, private_key
    ):
        if (api_key and not api_secret) or (not api_key and api_secret):
            raise InvalidAuthError(
                'Both api_key and api_secret must be set or both must be None.'
            )

        if (application_id and not private_key) or (not application_id and private_key):
            raise InvalidAuthError(
                'Both application_id and private_key must be set or both must be None.'
            )
