from vonage_utils.errors import VonageError


class VideoError(VonageError):
    """Indicates an error when using the Vonage Voice API."""


class InvalidRoleError(VideoError):
    """The specified role was invalid."""


class TokenExpiryError(VideoError):
    """The specified token expiry time was invalid."""


class SipError(VideoError):
    """Error related to usage of SIP calls."""


class NoAudioOrVideoError(VideoError):
    """Either an audio or video stream must be included."""


class IndividualArchivePropertyError(VideoError):
    """The property cannot be set for `archive_mode: 'individual'`."""


class LayoutStylesheetError(VideoError):
    """Error with the `stylesheet` property when setting a layout."""


class LayoutScreenshareTypeError(VideoError):
    """Error with the `screenshare_type` property when setting a layout."""


class InvalidArchiveStateError(VideoError):
    """The archive state was invalid for the specified operation."""


class InvalidHlsOptionsError(VideoError):
    """The HLS options were invalid."""


class InvalidOutputOptionsError(VideoError):
    """The output options were invalid."""


class InvalidBroadcastStateError(VideoError):
    """The broadcast state was invalid for the specified operation."""


class RoutedSessionRequiredError(VideoError):
    """The operation requires a session with `media_mode=routed`."""
