from vonage_utils.errors import VonageError


class VideoError(VonageError):
    """Indicates an error when using the Vonage Voice API."""


class InvalidRoleError(VideoError):
    """The specified role was invalid."""


class TokenExpiryError(VideoError):
    """The specified token expiry time was invalid."""


class SipError(VideoError):
    """Error related to usage of SIP calls."""
