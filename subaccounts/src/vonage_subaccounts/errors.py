from vonage_utils.errors import VonageError


class InvalidSecretError(VonageError):
    """Indicates that the secret provided was invalid."""
