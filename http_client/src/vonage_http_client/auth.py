import hashlib
import hmac
from base64 import b64encode
from time import time
from typing import Literal, Optional

from pydantic import validate_call
from vonage_jwt.jwt import JwtClient

from .errors import InvalidAuthError, JWTGenerationError


class Auth:
    """Deals with Vonage API authentication.

    Some Vonage APIs require an API key and secret for authentication. Others require an application ID and JWT.
    It is also possible to use a message signature with the SMS API.

    Args:
    - api_key (str): The API key for authentication.
    - api_secret (str): The API secret for authentication.
    - application_id (str): The application ID for JWT authentication.
    - private_key (str): The private key for JWT authentication.
    - signature_secret (str): The signature secret for authentication.
    - signature_method (str): The signature method for authentication.
        This should be one of `md5`, `sha1`, `sha256`, or `sha512` if using HMAC digests. If you want to use a simple MD5 hash, leave this as `None`.

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
        signature_secret: Optional[str] = None,
        signature_method: Optional[Literal['md5', 'sha1', 'sha256', 'sha512']] = 'md5',
    ) -> None:
        self._validate_input_combinations(
            api_key, api_secret, application_id, private_key, signature_secret
        )

        self._api_key = api_key
        self._api_secret = api_secret

        if application_id is not None and private_key is not None:
            self._jwt_client = JwtClient(application_id, private_key)

        self._signature_secret = signature_secret
        self._signature_method = getattr(hashlib, signature_method)

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

    def sign_params(self, params: dict) -> str:
        """Signs the provided message parameters using the signature secret provided to the `Auth`
        class. If no signature secret is provided, the message parameters are signed using a simple
        MD5 hash.

        Args:
            params (dict): The message parameters to be signed.

        Returns:
            str: A hexadecimal digest of the signed message parameters.
        """

        hasher = hmac.new(
            self._signature_secret.encode(),
            digestmod=self._signature_method,
        )

        if not params.get('timestamp'):
            params['timestamp'] = int(time())

        for key in sorted(params):
            value = params[key]

            if isinstance(value, str):
                value = value.replace('&', '_').replace('=', '_')

            hasher.update(f'&{key}={value}'.encode('utf-8'))

        return hasher.hexdigest()

    @validate_call
    def check_signature(self, params: dict) -> bool:
        """Checks the signature hash of the given parameters.

        Args:
            params (dict): The parameters to check the signature for.
                This should include the `sig` parameter which contains the
                signature hash of the other parameters.

        Returns:
            bool: True if the signature is valid, False otherwise.
        """
        signature = params.pop('sig', '').lower()
        return hmac.compare_digest(signature, self.sign_params(params))

    def _validate_input_combinations(
        self, api_key, api_secret, application_id, private_key, signature_secret
    ):
        if (api_secret or signature_secret) and not api_key:
            raise InvalidAuthError(
                '`api_key` must be set when `api_secret` or `signature_secret` is set.'
            )

        if api_key and not (api_secret or signature_secret):
            raise InvalidAuthError(
                'At least one of `api_secret` and `signature_secret` must be set if `api_key` is set.'
            )

        if (application_id and not private_key) or (not application_id and private_key):
            raise InvalidAuthError(
                'Both `application_id` and `private_key` must be set or both must be None.'
            )
