from typing import Literal, Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator

from .enums import Region
from .errors import ApplicationError


class ApplicationUrl(BaseModel):
    """URL for an application webhook.

    Args:
        address (str): The URL address.
        http_method (str, Optional): The HTTP method. Must be 'GET' or 'POST'.
    """

    address: str
    http_method: Optional[Literal['GET', 'POST']] = None


class VoiceUrl(ApplicationUrl):
    """Model with options to set URLs for a voice application webhook.

    Args:
        address (str): The URL address.
        http_method (str, Optional): The HTTP method. Must be 'GET' or 'POST'.
        connect_timeout (int, Optional): If Vonage can't connect to the webhook URL
            for this specified amount of time, then Vonage makes one additional attempt
            to connect to the webhook endpoint. This is an integer value specified in
            milliseconds.
        socket_timeout (int, Optional): If a response from the webhook URL can't be read
            for this specified amount of time, then Vonage makes one additional attempt
            to read the webhook endpoint. This is an integer value specified in
            milliseconds.
    """

    connect_timeout: Optional[int] = Field(None, ge=300, le=1000)
    socket_timeout: Optional[int] = Field(None, ge=1000, le=10000)


class VoiceWebhooks(BaseModel):
    """Voice application webhook URLs.

    Args:
        answer_url (VoiceUrl, Optional): The URL to which Vonage makes a request when a call
            is placed/received. This URL is used to provide the Nexmo Call Control Object
            (NCCO) that governs the call.
        fallback_answer_url (VoiceUrl, Optional): The URL to which Vonage makes a request when
            an error occurs in retrieving or executing the NCCO provided by the `answer_url`.
        event_url (VoiceUrl, Optional): The URL to which Vonage makes a request when a call
            event occurs.
    """

    answer_url: Optional[VoiceUrl] = None
    fallback_answer_url: Optional[VoiceUrl] = None
    event_url: Optional[VoiceUrl] = None


class Voice(BaseModel):
    """Voice application capabilities.

    Args:
        webhooks (VoiceWebhooks, Optional): Voice application webhook URLs.
        signed_callbacks (bool, Optional): Whether to sign the webhook callbacks.
        conversations_ttl (int, Optional): The length of time named conversations will
            remain active for after creation, in hours.
        leg_persistence_time (int, Optional):The persistence duration for legs, in days.
        region (Region, Optional): The region in which the application is hosted.
    """

    webhooks: Optional[VoiceWebhooks] = None
    signed_callbacks: Optional[bool] = None
    conversations_ttl: Optional[int] = Field(None, ge=1, le=9000)
    leg_persistence_time: Optional[int] = Field(None, ge=1, le=31)
    region: Optional[Region] = None


class RtcWebhooks(BaseModel):
    """Real-Time Communications application webhook URLs.

    Args:
        event_url (ApplicationUrl, Optional): The URL to which Vonage makes a request when
            an event occurs.
    """

    event_url: Optional[ApplicationUrl] = None


class Rtc(BaseModel):
    """Real-Time Communications application capabilities.

    Args:
        webhooks (RtcWebhooks, Optional): Real-Time Communications application webhook URLs.
        signed_callbacks (bool, Optional): Whether to sign the webhook callbacks.
    """

    webhooks: Optional[RtcWebhooks] = None
    signed_callbacks: Optional[bool] = None


class MessagesWebhooks(BaseModel):
    """Messages application webhook URLs.

    Args:
        inbound_url (ApplicationUrl, Optional): The URL Vonage forwards inbound messages
            to when they are received.
        status_url (ApplicationUrl, Optional): The URL where Vonage sends events related to
            your messages.
    """

    inbound_url: Optional[ApplicationUrl] = None
    status_url: Optional[ApplicationUrl] = None

    @field_validator('inbound_url', 'status_url')
    @classmethod
    def check_http_method(cls, v: ApplicationUrl):
        if v.http_method is not None and v.http_method != 'POST':
            raise ApplicationError('HTTP method must be POST')
        return v


class Messages(BaseModel):
    """Messages application capabilities.

    Args:
        webhooks (MessagesWebhooks, Optional): Messages application webhook URLs.
        version (str, Optional): The version of the Messages API to use.
        authenticate_inbound_media (bool, Optional): Whether to authenticate inbound media.
    """

    webhooks: Optional[MessagesWebhooks] = None
    version: Optional[str] = None
    authenticate_inbound_media: Optional[bool] = None


class Vbc(BaseModel):
    """VBC capabilities.

    This object should be empty when creating or updating an application.
    """


class VerifyWebhooks(BaseModel):
    """Verify application webhook URLs.

    Args:
        status_url (ApplicationUrl, Optional): The URL to which Vonage makes a request when
            a verification event occurs.
    """

    status_url: Optional[ApplicationUrl] = None

    @field_validator('status_url')
    @classmethod
    def check_http_method(cls, v: ApplicationUrl):
        if v.http_method is not None and v.http_method != 'POST':
            raise ApplicationError('HTTP method must be POST')
        return v


class Verify(BaseModel):
    """Verify application capabilities.

    Don't set the `version` field when creating or updating an application.

    Args:
        webhooks (VerifyWebhooks, Optional): Verify application webhook URLs.
    """

    webhooks: Optional[VerifyWebhooks] = None
    version: Optional[str] = None


class Privacy(BaseModel):
    """Privacy settings for an application.

    Args:
        improve_ai (bool, Optional): If set to true, Vonage may store and use your
            content and data for the improvement of Vonage's AI based services and
            technologies.
    """

    improve_ai: Optional[bool] = None


class Capabilities(BaseModel):
    """Application capabilities.

    Args:
        voice (Voice, Optional): Voice application capabilities.
        rtc (Rtc, Optional): Real-Time Communications application capabilities.
        messages (Messages, Optional): Messages application capabilities.
        vbc (Vbc, Optional): VBC capabilities.
        verify (Verify, Optional): Verify application capabilities.
    """

    voice: Optional[Voice] = None
    rtc: Optional[Rtc] = None
    messages: Optional[Messages] = None
    vbc: Optional[Vbc] = None
    verify: Optional[Verify] = None


class Keys(BaseModel):
    """Application keys.

    Args:
        public_key (str, Optional): The public key.
    """

    model_config = ConfigDict(extra='allow')

    public_key: Optional[str] = None


class ApplicationBase(BaseModel):
    """Base application object used in requests and responses when communicating with the
    Vonage Application API.

    Args:
        name (str): The name of the application.
        capabilities (Capabilities, Optional): The capabilities of the application.
        privacy (Privacy, Optional): The privacy settings for the application.
        keys (Keys, Optional): The application keys.
    """

    name: str
    capabilities: Optional[Capabilities] = None
    privacy: Optional[Privacy] = None
    keys: Optional[Keys] = None
