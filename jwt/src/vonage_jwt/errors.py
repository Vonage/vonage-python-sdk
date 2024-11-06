from vonage_utils import VonageError


class VonageJwtError(VonageError):
    """An error relating to the Vonage JWT Generator."""


class VonageVerifyJwtError(VonageError):
    """The signature could not be verified."""
