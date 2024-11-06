from typing import Optional

from pydantic import BaseModel, Field, model_validator

from .enums import ArchiveMode, MediaMode, P2pPreference


class SessionOptions(BaseModel):
    """Options for creating a new session.

    Args:
        media_mode (MediaMode): The media mode for the session.
        archive_mode (ArchiveMode): The archive mode for the session.
        location (str): The location of the session.
        e2ee (bool): Whether end-to-end encryption is enabled.
        p2p_preference (str): The preference for peer-to-peer connections.
            This is set automatically by selecting the `media_mode`.
    """

    archive_mode: Optional[ArchiveMode] = Field(None, serialization_alias='archiveMode')
    location: Optional[str] = None
    media_mode: Optional[MediaMode] = None
    e2ee: Optional[bool] = None
    p2p_preference: Optional[str] = Field(
        P2pPreference.DISABLED, serialization_alias='p2p.preference'
    )

    @model_validator(mode='after')
    def set_p2p_preference(self):
        if self.media_mode == MediaMode.ROUTED:
            self.p2p_preference = P2pPreference.DISABLED
        if self.media_mode == MediaMode.RELAYED:
            self.p2p_preference = P2pPreference.ALWAYS
        return self

    @model_validator(mode='after')
    def set_p2p_preference_if_archive_mode_set(self):
        if self.archive_mode == ArchiveMode.ALWAYS:
            self.p2p_preference = P2pPreference.DISABLED
        return self


class VideoSession(BaseModel):
    """The new session ID and options specified in the request.

    Args:
        session_id (str): The session ID.
        archive_mode (ArchiveMode, Optional): The archive mode for the session.
        media_mode (MediaMode, Optional): The media mode for the session.
        location (str, Optional): The location of the session.
        e2ee (bool, Optional): Whether end-to-end encryption is enabled for the session.
    """

    session_id: str
    archive_mode: Optional[ArchiveMode] = None
    media_mode: Optional[MediaMode] = None
    location: Optional[str] = None
    e2ee: Optional[bool] = None
