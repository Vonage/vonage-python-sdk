from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel


class InsightStatus(BaseModel):
    """Model for the status of an individual insight response.

    Args:
        code (str): Status code of the insight processing.
        message (str, Optional): Human-readable description of the status.
    """

    code: str
    message: Optional[str]


class FormatInsightResponse(BaseModel):
    """Model for the response of the `format` insight.

    This insight validates the phone number format and provides information
    derived from its numbering plan.

    Args:
        country_code (str, Optional): Country code in ISO 3166-1 alpha-2 format.
        country_name (str, Optional): Full country name.
        country_prefix (str, Optional): Numeric country calling code.
        offline_location (str, Optional): Location derived from the number prefix.
        time_zones (List[str], Optional): Time zones associated with the number.
        number_international (str, Optional): Phone number in E.164 format.
        number_national (str, Optional): Phone number in national format.
        is_format_valid (bool, Optional): Indicates whether the number format is valid.
        status (InsightStatus): Processing status of the insight.
    """

    country_code: Optional[str]
    country_name: Optional[str]
    country_prefix: Optional[str]
    offline_location: Optional[str]
    time_zones: Optional[List[str]]
    number_international: Optional[str]
    number_national: Optional[str]
    is_format_valid: Optional[bool]
    status: InsightStatus


class SimSwapInsightResponse(BaseModel):
    """Model for the response of the `sim_swap` insight.

    This insight indicates whether a SIM swap has occurred recently.

    Args:
        latest_sim_swap_at (datetime, Optional): Timestamp of the most recent
            SIM swap, in UTC.
        is_swapped (bool, Optional): Indicates whether a SIM swap occurred
            within the requested period.
        status (InsightStatus): Processing status of the insight.
    """

    latest_sim_swap_at: Optional[datetime] = None
    is_swapped: Optional[bool] = None
    status: InsightStatus


class OriginalCarrierInsightResponse(BaseModel):
    """Model for the response of the `original_carrier` insight.

    Provides information about the network to which the phone number was
    originally assigned.

    Args:
        name (str, Optional): Full name of the original carrier.
        network_type (str, Optional): Type of the network (e.g. MOBILE, LANDLINE).
        country_code (str, Optional): Country code in ISO 3166-1 alpha-2 format.
        network_code (str, Optional): MCC + MNC network identifier.
        status (InsightStatus): Processing status of the insight.
    """

    name: Optional[str]
    network_type: Optional[str]
    country_code: Optional[str]
    network_code: Optional[str]
    status: InsightStatus


class CurrentCarrierInsightResponse(BaseModel):
    """Model for the response of the `current_carrier` insight.

    Provides information about the network the phone number is currently
    assigned to.

    Args:
        name (str, Optional): Full name of the current carrier.
        network_type (str, Optional): Type of the network (e.g. MOBILE).
        country_code (str, Optional): Country code in ISO 3166-1 alpha-2 format.
        network_code (str, Optional): MCC + MNC network identifier.
        status (InsightStatus): Processing status of the insight.
    """

    name: Optional[str]
    network_type: Optional[str]
    country_code: Optional[str]
    network_code: Optional[str]
    status: InsightStatus


class LocationVerificationInsightResponse(BaseModel):
    """Model for the response of the `location_verification` insight.

    Indicates whether the device associated with the phone number is located
    within the requested geographic area.

    Args:
        is_verified (str, Optional): Verification result (TRUE, FALSE, PARTIAL, UNKNOWN).
        latest_location_at (datetime, Optional): Timestamp of the latest
            location update, in UTC.
        match_rate (int, Optional): Percentage indicating the degree of overlap
            between requested and detected locations.
        status (InsightStatus): Processing status of the insight.
    """

    is_verified: Optional[str]
    latest_location_at: Optional[datetime]
    match_rate: Optional[int]
    status: InsightStatus


class SubscriberMatchInsightResponse(BaseModel):
    """Model for the response of the `subscriber_match` insight.

    Provides matching results between customer-provided identity attributes
    and the operator's verified records.

    Args:
        id_document_match (str, Optional): Match result for the ID document.
        given_name_match (str, Optional): Match result for the given name.
        family_name_match (str, Optional): Match result for the family name.
        address_match (str, Optional): Match result for the full address.
        street_name_match (str, Optional): Match result for the street name.
        street_number_match (str, Optional): Match result for the street number.
        postal_code_match (str, Optional): Match result for the postal code.
        locality_match (str, Optional): Match result for the locality.
        region_match (str, Optional): Match result for the region.
        country_match (str, Optional): Match result for the country.
        house_number_extension_match (str, Optional): Match result for the
            house number extension.
        birthdate_match (str, Optional): Match result for the birthdate.
        status (InsightStatus): Processing status of the insight.
    """

    id_document_match: Optional[str]
    given_name_match: Optional[str]
    family_name_match: Optional[str]
    address_match: Optional[str]
    street_name_match: Optional[str]
    street_number_match: Optional[str]
    postal_code_match: Optional[str]
    locality_match: Optional[str]
    region_match: Optional[str]
    country_match: Optional[str]
    house_number_extension_match: Optional[str]
    birthdate_match: Optional[str]
    status: InsightStatus


class RoamingInsightResponse(BaseModel):
    """Model for the response of the `roaming` insight.

    Indicates whether the device is currently roaming and the associated
    roaming countries.

    Args:
        latest_status_at (datetime, Optional): Timestamp of the latest roaming
            status update, in UTC.
        is_roaming (bool, Optional): Indicates whether the device is roaming.
        country_codes (List[str], Optional): Country codes where the device
            is roaming.
        status (InsightStatus): Processing status of the insight.
    """

    latest_status_at: Optional[datetime]
    is_roaming: Optional[bool]
    country_codes: Optional[List[str]]
    status: InsightStatus


class ReachabilityInsightResponse(BaseModel):
    """Model for the response of the `reachability` insight.

    Indicates whether the device is reachable on the mobile network.

    Args:
        latest_status_at (datetime, Optional): Timestamp of the latest
            reachability update, in UTC.
        is_reachable (bool, Optional): Indicates whether the device is reachable.
        connectivity (List[str], Optional): Connectivity types available
            (e.g. DATA, SMS).
        status (InsightStatus): Processing status of the insight.
    """

    latest_status_at: Optional[datetime]
    is_reachable: Optional[bool]
    connectivity: Optional[List[str]]
    status: InsightStatus


class InsightsResponse(BaseModel):
    """Model for the collection of identity insight responses.

    Each field corresponds to an insight requested in the original request.
    Only insights that were requested will be present in the response.

    Args:
        format (FormatInsightResponse, Optional): Format validation response.
        sim_swap (SimSwapInsightResponse, Optional): SIM swap response.
        original_carrier (OriginalCarrierInsightResponse, Optional): Original
            carrier response.
        current_carrier (CurrentCarrierInsightResponse, Optional): Current
            carrier response.
        location_verification (LocationVerificationInsightResponse, Optional):
            Location verification response.
        subscriber_match (SubscriberMatchInsightResponse, Optional): Subscriber
            match response.
        roaming (RoamingInsightResponse, Optional): Roaming status response.
        reachability (ReachabilityInsightResponse, Optional): Reachability response.
    """

    format: Optional[FormatInsightResponse] = None
    sim_swap: Optional[SimSwapInsightResponse] = None
    original_carrier: Optional[OriginalCarrierInsightResponse] = None
    current_carrier: Optional[CurrentCarrierInsightResponse] = None
    location_verification: Optional[LocationVerificationInsightResponse] = None
    subscriber_match: Optional[SubscriberMatchInsightResponse] = None
    roaming: Optional[RoamingInsightResponse] = None
    reachability: Optional[ReachabilityInsightResponse] = None


class IdentityInsightsResponse(BaseModel):
    """Model for an Identity Insights API response.

    Represents the aggregated response containing the results of all requested
    identity insights.

    Args:
        request_id (str, Optional): Unique identifier for the request.
        insights (InsightsResponse): Collection of insight responses.
    """

    request_id: Optional[str] = None
    insights: InsightsResponse
