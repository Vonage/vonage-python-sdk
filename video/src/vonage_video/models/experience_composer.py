from typing import Optional

from pydantic import BaseModel, Field
from vonage_video.models.enums import ExperienceComposerStatus, VideoResolution


class ExperienceComposerProperties(BaseModel):
    """Model with properties for an Experience Composer session.

    Args:
        name (str): The name of the composed output stream which is published to the session.
    """

    name: str = Field(..., min_length=1, max_length=200)


class ExperienceComposerOptions(BaseModel):
    """The options for the Experience Composer.

    Args:
        session_id (str): The session ID of the Vonage Video session you are working with.
        token (str): A valid Vonage Video JWT with a Publisher role and (optionally) connection data to be associated with the output stream.
        url (str, Optional): A publicly reachable URL controlled by the customer and capable of generating the content to be rendered without user intervention.
        max_duration (int, Optional): The maximum duration.
        resolution (ExperienceComposerResolution, Optional): The resolution of the Experience Composer stream.
        properties (ExperienceComposerProperties, Optional): The initial configuration of Publisher properties for the composed output stream.
    """

    session_id: str = Field(..., serialization_alias='sessionId')
    token: str
    url: str = Field(..., min_length=15, max_length=2048)
    max_duration: Optional[int] = Field(
        None, ge=60, le=36000, serialization_alias='maxDuration'
    )
    resolution: Optional[VideoResolution] = None
    properties: Optional[ExperienceComposerProperties] = None


class ExperienceComposer(BaseModel):
    """Model with data describing an Experience Composer session.

    Args:
        id (str, Optional): The unique ID for the Experience Composer.
        session_id (str, Optional): The session ID of the Vonage Video session you are working with.
        application_id (str, Optional): The Vonage application ID.
        created_at (int, Optional): The time the Experience Composer started, expressed in milliseconds since the Unix epoch (January 1, 1970, 00:00:00 UTC).
        callback_url (str, Optional): The callback URL for Experience Composer events (if one was set).
        updated_at (int, Optional): The UNIX timestamp when the Experience Composer status was last updated.
        name (str, Optional): The name of the composed output stream which is published to the session.
        url (str, Optional): A publicly reachable URL controlled by the customer and capable of generating the content to be rendered without user intervention.
        resolution (ExperienceComposerResolution, Optional): The resolution of the Experience Composer stream.
        status (ExperienceComposerStatus, Optional): The status.
        stream_id (str, Optional): The ID of the composed stream being published.
        reason (str, Optional): The reason for the status change.
    """

    id: Optional[str] = None
    session_id: Optional[str] = Field(None, validation_alias='sessionId')
    application_id: Optional[str] = Field(None, validation_alias='applicationId')
    created_at: Optional[int] = Field(None, validation_alias='createdAt')
    callback_url: Optional[str] = Field(None, validation_alias='callbackUrl')
    updated_at: Optional[int] = Field(None, validation_alias='updatedAt')
    name: Optional[str] = None
    url: Optional[str] = None
    resolution: Optional[VideoResolution] = None
    status: Optional[ExperienceComposerStatus] = None
    stream_id: Optional[str] = Field(None, validation_alias='streamId')
    reason: Optional[str] = None


class ListExperienceComposersFilter(BaseModel):
    """Request object for filtering Experience Composers associated with the specific
    Vonage application.

    Args:
        offset (int, Optional): The offset.
        page_size (int, Optional): The number of Experience Composers to return.
    """

    offset: Optional[int] = None
    page_size: Optional[int] = Field(100, serialization_alias='count')
