from typing import Optional

from pydantic import BaseModel


class StartVerificationResponse(BaseModel):
    """Response object for starting a verification process.

    Args:
        request_id (str): The unique ID of the Verify request. You need this `request_id`
            for the Verify check.
        status (str): Indicates the outcome of the request; zero is success.
    """

    request_id: str
    status: str


class CheckCodeResponse(BaseModel):
    """Response object for checking a verification code.

    Args:
        request_id (str): The unique ID of the Verify request to check.
        status (str): Indicates the outcome of the request; zero is success.
        event_id (str): The ID of the verification event, such as an SMS or TTS call.
        price (str): The cost incurred for this request.
        currency (str): The currency code.
        estimated_price_messages_sent (str, Optional): Cost (in EUR) of the calls made
            and messages sent for the verification process.
    """

    request_id: str
    status: str
    event_id: str
    price: str
    currency: str
    estimated_price_messages_sent: Optional[str] = None


class Check(BaseModel):
    """The list of checks made for a specific verification and their outcomes.

    Args:
        date_received (str, Optional): The date and time this check was received (in the
            format YYYY-MM-DD HH:MM:SS)
        code (str, Optional): The code supplied with this check request.
        status (str, Optional): The status of the check.
        ip_address (str, Optional): The IP address of the check. This field is no longer
            used.
    """

    date_received: Optional[str] = None
    code: Optional[str] = None
    status: Optional[str] = None
    ip_address: Optional[str] = None


class Event(BaseModel):
    """The events that have taken place to verify this number, and their unique
    identifiers.

    Args:
        type (str, Optional): The type of event.
        id (str, Optional): The ID of the event.
    """

    type: Optional[str] = None
    id: Optional[str] = None


class VerifyStatus(BaseModel):
    """The status of a verification request.

    Args:
        request_id (str, Optional): The `request_id` that you received in the response to
            the Verify request and used in the Verify search request.
        account_id (str, Optional): The Vonage account ID the request was for.
        status (str, Optional): The status of the verification request.
        number (str, Optional): The phone number used in the request.
        price (str, Optional): The cost of this verification.
        currency (str, Optional): The currency code.
        sender_id (str, Optional): The sender ID provided in the Verify request.
        date_submitted (str, Optional): The date and time this verification request was
            submitted (in the format YYYY-MM-DD HH:MM:SS).
        date_finalized (str, Optional): The date and time this verification request was
            completed (in the format YYYY-MM-DD HH:MM:SS).
        first_event_date (str, Optional): The date and time of the first verification
            attempt (in the format YYYY-MM-DD HH:MM:SS).
        last_event_date (str, Optional): The date and time of the last verification
            attempt (in the format YYYY-MM-DD HH:MM:SS).
        checks (list[Check], Optional): The list of checks made for this verification and
            their outcomes.
        events (list[Event], Optional): The events that have taken place to verify this
            number, and their unique identifiers.
        estimated_price_messages_sent (str, Optional): Cost (in EUR) of the calls made
            and messages sent for the verification process.
    """

    request_id: Optional[str] = None
    account_id: Optional[str] = None
    status: Optional[str] = None
    number: Optional[str] = None
    price: Optional[str] = None
    currency: Optional[str] = None
    sender_id: Optional[str] = None
    date_submitted: Optional[str] = None
    date_finalized: Optional[str] = None
    first_event_date: Optional[str] = None
    last_event_date: Optional[str] = None
    checks: Optional[list[Check]] = None
    events: Optional[list[Event]] = None
    estimated_price_messages_sent: Optional[str] = None


class VerifyControlStatus(BaseModel):
    """The status of a verification control request.

    Args:
        status (str): The status of the control request.
        command (str): The command that was requested when cancelling a verify request
            or triggering the next workflow in a request.
    """

    status: str
    command: str


class NetworkUnblockStatus(BaseModel):
    """The status of a network unblock request.

    Args:
        network (str): The unique network ID of the network that was unblocked.
        unblocked_until (str): The date and time until which the network is unblocked.
    """

    network: str
    unblocked_until: str
