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
    message: Optional[str] = None


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

    country_code: Optional[str] = None
    country_name: Optional[str] = None
    country_prefix: Optional[str] = None
    offline_location: Optional[str] = None
    time_zones: Optional[List[str]] = None
    number_international: Optional[str] = None
    number_national: Optional[str] = None
    is_format_valid: Optional[bool] = None
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


class CarrierInsightResponse(BaseModel):
    """Model for the response of the `original_carrier` and `current_carrier` insights.

    Provides information about the network to which the phone number was
    originally assigned.

    Args:
        name (str, Optional): Full name of the original carrier.
        network_type (str, Optional): Type of the network (e.g. MOBILE, LANDLINE).
        country_code (str, Optional): Country code in ISO 3166-1 alpha-2 format.
        network_code (str, Optional): MCC + MNC network identifier.
        status (InsightStatus): Processing status of the insight.
    """

    name: Optional[str] = None
    network_type: Optional[str] = None
    country_code: Optional[str] = None
    network_code: Optional[str] = None
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
    original_carrier: Optional[CarrierInsightResponse] = None
    current_carrier: Optional[CarrierInsightResponse] = None


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
