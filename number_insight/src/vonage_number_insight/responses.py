from typing import Literal, Optional, Union

from pydantic import BaseModel


class BasicInsightResponse(BaseModel):
    """Model for a basic number insight response.

    Args:
        status (int, Optional): The status code of the request.
        status_message (str, Optional): The status message of the request.
        request_id (str, Optional): The unique identifier for the request.
        international_format_number (str, Optional): The international format of the phone
            number in your request.
        national_format_number (str, Optional): The national format of the phone number
            in your request.
        country_code (str, Optional): The 2-character country code of the phone number in
            your request. This is in ISO 3166-1 alpha-2 format.
        country_code_iso3 (str, Optional): The 3-character country code of the phone number
            in your request. This is in ISO 3166-1 alpha-3 format.
        country_name (str, Optional): The name of the country that the phone number is
            registered in.
        country_prefix (str, Optional): The numeric prefix for the country that the phone
            number is registered in.
    """

    status: int = None
    status_message: str = None
    request_id: Optional[str] = None
    international_format_number: Optional[str] = None
    national_format_number: Optional[str] = None
    country_code: Optional[str] = None
    country_code_iso3: Optional[str] = None
    country_name: Optional[str] = None
    country_prefix: Optional[str] = None


class Carrier(BaseModel):
    """Model for the carrier information of a phone number. While in some cases and
    regions it may return information for non-mobile numbers, this field is supported only
    for mobile numbers.

    Args:
        network_code (str, Optional): The Mobile Country Code for the carrier the number
            is associated with. Unreal numbers are marked as null and the request is
            rejected altogether if the number is impossible according to the E.164 guidelines.
        name (str, Optional): The full name of the carrier.
        country (str, Optional): The country that the carrier is registered in.
            This is in ISO 3166-1 alpha-2 format.
        network_type (str, Optional): The type of network the number is associated with.
    """

    network_code: Optional[str] = None
    name: Optional[str] = None
    country: Optional[str] = None
    network_type: Optional[str] = None


class CallerIdentity(BaseModel):
    """Model for the caller identity information of a phone number. Only included if
    `cnam=True` in the request.

    Args:
        caller_type (str, Optional): The type of caller. Possible values are "business"
            or "consumer".
        caller_name (str, Optional): Full name of the person or business who owns the
            phone number.
        first_name (str, Optional): The first name of the caller if an individual.
        last_name (str, Optional): The last name of the caller if an individual.
        subscription_type (str, Optional): The type of subscription the caller has.
    """

    caller_type: Optional[str] = None
    caller_name: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    subscription_type: Optional[str] = None


class StandardInsightResponse(BasicInsightResponse):
    """Model for a standard number insight response.

    Args:
        request_price (str, Optional): The price in EUR charged for the request.
        refund_price (str, Optional): The price in EUR that will be refunded to your
            account in case the request is not successful.
        remaining_balance (str, Optional): The remaining balance in your account in EUR.
        current_carrier (Carrier, Optional): Information about the network `number` is
            currently connected to. While in some cases and regions it may return
            information for non-mobile numbers, this field is supported only for mobile
            numbers.
        original_carrier (Carrier, Optional): Information about the network `number` was
            initially connected to.
        ported (str, Optional): If the user has changed carrier for `number`. The assumed
            status means that the information supplier has replied to the request but has
            not said explicitly that the number is ported.
        caller_identity (CallerIdentity, Optional): Information about the caller. Only
            included if `cnam=True` in the request.
        status (int, Optional): The status code of the request.
        status_message (str, Optional): The status message of the request.
        request_id (str, Optional): The unique identifier for the request.
        international_format_number (str, Optional): The international format of the phone
            number in your request.
        national_format_number (str, Optional): The national format of the phone number
            in your request.
        country_code (str, Optional): The 2-character country code of the phone number in
            your request. This is in ISO 3166-1 alpha-2 format.
        country_code_iso3 (str, Optional): The 3-character country code of the phone number
            in your request. This is in ISO 3166-1 alpha-3 format.
        country_name (str, Optional): The name of the country that the phone number is
            registered in.
        country_prefix (str, Optional): The numeric prefix for the country that the phone
            number is registered in.
    """

    request_price: Optional[str] = None
    refund_price: Optional[str] = None
    remaining_balance: Optional[str] = None
    current_carrier: Optional[Carrier] = None
    original_carrier: Optional[Carrier] = None
    ported: Optional[str] = None
    caller_identity: Optional[CallerIdentity] = None


class RoamingStatus(BaseModel):
    """Model for the roaming status of a phone number.

    Args:
        status (str, Optional): The roaming status of the phone number.
        roaming_country_code (str, Optional): If the number is roaming, this is the country
            code of the country the number is roaming in.
        roaming_network_code (str, Optional): If the number is roaming, this is the ID of
            the carrier network the number is roaming with.
        roaming_network_name (str, Optional): If roaming, this is the name of the carrier
            network the number is roaming in.
    """

    status: Optional[str] = None
    roaming_country_code: Optional[str] = None
    roaming_network_code: Optional[str] = None
    roaming_network_name: Optional[str] = None


class AdvancedSyncInsightResponse(StandardInsightResponse):
    """Model for an advanced synchronous number insight response.

    Args:
        roaming (RoamingStatus, Optional): Information about the roaming status of the phone
            number.
        lookup_outcome (int, Optional): Shows if all information about the number
            has been returned.
        lookup_outcome_message (str, Optional): Status message about the lookup outcome.
        valid_number (str, Optional): The validity of the phone number.
        reachable (str, Optional): The reachability of the phone number. Only applies
            to mobile numbers.
        request_price (str, Optional): The price in EUR charged for the request.
        refund_price (str, Optional): The price in EUR that will be refunded to your
            account in case the request is not successful.
        remaining_balance (str, Optional): The remaining balance in your account in EUR.
        current_carrier (Carrier, Optional): Information about the network `number` is
            currently connected to. While in some cases and regions it may return
            information for non-mobile numbers, this field is supported only for mobile
            numbers.
        original_carrier (Carrier, Optional): Information about the network `number` was
            initially connected to.
        ported (str, Optional): If the user has changed carrier for `number`. The assumed
            status means that the information supplier has replied to the request but has
            not said explicitly that the number is ported.
        caller_identity (CallerIdentity, Optional): Information about the caller. Only
            included if `cnam=True` in the request.
        status (int, Optional): The status code of the request.
        status_message (str, Optional): The status message of the request.
        request_id (str, Optional): The unique identifier for the request.
        international_format_number (str, Optional): The international format of the phone
            number in your request.
        national_format_number (str, Optional): The national format of the phone number
            in your request.
        country_code (str, Optional): The 2-character country code of the phone number in
            your request. This is in ISO 3166-1 alpha-2 format.
        country_code_iso3 (str, Optional): The 3-character country code of the phone number
            in your request. This is in ISO 3166-1 alpha-3 format.
        country_name (str, Optional): The name of the country that the phone number is
            registered in.
        country_prefix (str, Optional): The numeric prefix for the country that the phone
            number is registered in.
    """

    roaming: Optional[Union[RoamingStatus, Literal['unknown']]] = None
    lookup_outcome: Optional[int] = None
    lookup_outcome_message: Optional[str] = None
    valid_number: Optional[str] = None
    reachable: Optional[str] = None


class AdvancedAsyncInsightResponse(BaseModel):
    """Model for an advanced asynchronous number insight response.

    Args:
        request_id (str, Optional): The unique identifier for the request.
        number (str, Optional): The phone number to get insight information for.
        remaining_balance (str, Optional): The remaining balance in your account in EUR.
        request_price (str, Optional): The price in EUR charged for the request.
        status (int, Optional): The status code of the request.
        error_text (str, Optional): The status description of the request.
    """

    request_id: Optional[str] = None
    number: Optional[str] = None
    remaining_balance: Optional[str] = None
    request_price: Optional[str] = None
    status: Optional[int] = None
    error_text: Optional[str] = None
