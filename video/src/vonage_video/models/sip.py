from typing import Optional

from pydantic import BaseModel, Field


class SipAuth(BaseModel):
    """Model representing the authentication details for the SIP INVITE request for HTTP
    digest authentication, if it is required by your SIP platform.

    Args:
        username (str): The username for HTTP digest authentication.
        password (str): The password for HTTP digest authentication.
    """

    username: str
    password: str


class SipOptions(BaseModel):
    """Model representing the SIP options for the call.

    Args:
        uri (str): The SIP URI to be used as the destination of the SIP call.
        from_ (Optional[str]): The number or string sent to the final SIP number
            as the caller. It must be a string in the form of `from@example.com`, where
            `from` can be a string or a number.
        headers (Optional[dict]): Custom headers to be added to the SIP INVITE request.
        auth (Optional[SipAuth]): Authentication details for the SIP INVITE request.
        secure (Optional[bool]): Indicates whether the media must be transmitted encrypted.
            Default is false.
        video (Optional[bool]): Indicates whether the SIP call will include video.
            Default is false.
        observe_force_mute (Optional[bool]): Indicates whether the SIP endpoint observes
            force mute moderation.
    """

    uri: str
    from_: Optional[str] = Field(None, serialization_alias='from')
    headers: Optional[dict] = None
    auth: Optional[SipAuth] = None
    secure: Optional[bool] = None
    video: Optional[bool] = None
    observe_force_mute: Optional[bool] = Field(
        None, serialization_alias='observeForceMute'
    )


class InitiateSipRequest(BaseModel):
    """Model representing the SIP options for joining a Vonage Video session.

    Args:
        session_id (str): The Vonage Video session ID for the SIP call to join.
        token (str): The Vonage Video token to be used for the participant being called.
        sip (Sip): The SIP options for the call.
    """

    session_id: str = Field(..., serialization_alias='sessionId')
    token: str
    sip: SipOptions


class SipCall(BaseModel):
    """Model representing the details of a SIP call.

    Args:
        id (str): A unique ID for the SIP call.
        project_id (str): The Vonage Video project ID for the SIP call.
        session_id (str): The Vonage Video session ID for the SIP call.
        connection_id (str): The Vonage Video connection ID for the SIP call's connection
            in the Vonage Video session.
        stream_id (str): The Vonage Video stream ID for the SIP call's stream in the
            Vonage Video session.
        created_at (int): The timestamp when the SIP call was created,in milliseconds since
            the Unix epoch.
        updated_at (int): The timestamp when the SIP call was last updated, in milliseconds
            since the Unix epoch.
    """

    id: Optional[str] = None
    project_id: Optional[str] = Field(None, validation_alias='projectId')
    session_id: Optional[str] = Field(None, validation_alias='sessionId')
    connection_id: str = Field(None, validation_alias='connectionId')
    stream_id: str = Field(None, validation_alias='streamId')
    created_at: Optional[int] = Field(None, validation_alias='createdAt')
    updated_at: Optional[int] = Field(None, validation_alias='updatedAt')
