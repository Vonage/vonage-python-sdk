from vonage_utils.errors import VonageError


class VoiceError(VonageError):
    """Indicates an error when using the Vonage Voice API."""


class NccoActionError(VoiceError):
    """Indicates an error when using an NCCO action."""
