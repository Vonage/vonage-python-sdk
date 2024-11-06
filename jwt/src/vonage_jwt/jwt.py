import re
from copy import deepcopy
from time import time
from typing import Union
from uuid import uuid4

from jwt import encode

from .errors import VonageJwtError


class JwtClient:
    """Object used to pass in an application ID and private key to generate JWT
    methods."""

    def __init__(self, application_id: str, private_key: str):
        self._application_id = application_id

        try:
            self._set_private_key(private_key)
        except Exception as err:
            raise VonageJwtError(err)

        if self._application_id is None or self._private_key is None:
            raise VonageJwtError(
                'Both of "application_id" and "private_key" are required.'
            )

    def generate_application_jwt(self, jwt_options: dict = None) -> bytes:
        """Generates a JWT for the specified Vonage application.

        You can override values for application_id and private_key on the JWTClient object by
        specifying them in the `jwt_options` dict if required.

        Args:
            jwt_options (dict): The options to include in the JWT.

        Returns:
            bytes: The generated JWT.
        """
        if jwt_options is None:
            jwt_options = {}

        iat = int(time())

        payload = deepcopy(jwt_options)
        payload["application_id"] = self._application_id
        payload['iat'] = payload.get("iat", iat)
        payload["jti"] = payload.get("jti", str(uuid4()))
        payload["exp"] = payload.get("exp", payload["iat"] + (15 * 60))

        headers = {'alg': 'RS256', 'typ': 'JWT'}

        token = encode(payload, self._private_key, algorithm='RS256', headers=headers)
        return bytes(token, 'utf-8')

    def _set_private_key(self, key: Union[str, bytes]) -> None:
        if isinstance(key, (str, bytes)) and re.search("[.][a-zA-Z0-9_]+$", key):
            with open(key, "rb") as key_file:
                self._private_key = key_file.read()
        elif isinstance(key, str) and '-----BEGIN PRIVATE KEY-----' not in key:
            raise VonageJwtError(
                "If passing the private key directly as a string, it must be formatted correctly with newlines."
            )
        else:
            self._private_key = key
