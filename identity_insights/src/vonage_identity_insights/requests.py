from typing import Optional, Literal
from datetime import date

from pydantic import BaseModel, Field
from vonage_utils.types import PhoneNumber


class EmptyInsight(BaseModel):
    """Model for an insight request without parameters.

    This model represents insights that must be included as an empty JSON
    object (`{}`) to indicate that the insight is requested.
    """

    pass


class SimSwapInsight(BaseModel):
    """Model for a SIM swap insight request.

    This insight checks whether a SIM swap has occurred within a specified
    period of time.

    Args:
        period (int, Optional): Period in hours to be checked for SIM swap.
            Must be between 1 and 2400. Defaults to 240.
    """

    period: Optional[int] = Field(
        default=240,
        ge=1,
        le=2400,
        description="Period in hours to be checked for SIM swap",
    )


class SubscriberMatchInsight(BaseModel):
    """Model for a subscriber match insight request.

    This insight compares customer-provided identity attributes with those
    stored and verified by the mobile network operator.

    At least one attribute must be provided.

    Args:
        id_document (str, Optional): Identifier from the customer's official
            identity document.
        given_name (str, Optional): First or given name of the customer.
        family_name (str, Optional): Last name or family name of the customer.
        street_name (str, Optional): Name of the street in the customer's address.
        street_number (str, Optional): Street number of the customer's address.
        postal_code (str, Optional): Postal or ZIP code of the customer's address.
        locality (str, Optional): City or locality of the customer's address.
        region (str, Optional): Region or prefecture of the customer's address.
        country (str, Optional): Country code of the customer's address
            (ISO 3166-1 alpha-2).
        house_number_extension (str, Optional): Additional house identifier
            (e.g. apartment or suite number).
        birthdate (date, Optional): Birthdate of the customer in ISO 8601 format.
    """

    id_document: Optional[str]
    given_name: Optional[str]
    family_name: Optional[str]
    street_name: Optional[str]
    street_number: Optional[str]
    postal_code: Optional[str]
    locality: Optional[str]
    region: Optional[str]
    country: Optional[str]
    house_number_extension: Optional[str]
    birthdate: Optional[date]


class LocationCenter(BaseModel):
    """Model for the center point of a geographic area.

    Args:
        latitude (float): Latitude of the center point, in decimal degrees.
            Must be between -90 and 90.
        longitude (float): Longitude of the center point, in decimal degrees.
            Must be between -180 and 180.
    """

    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)


class Location(BaseModel):
    """Model for a geographic area definition.

    Currently, only circular areas are supported.

    Args:
        type (Literal["CIRCLE"]): Type of the geographic area.
        radius (int): Radius of the area in meters. Must be between 2000 and
            200000.
        center (LocationCenter): Center point of the area.
    """

    type: Literal["CIRCLE"]
    radius: int = Field(..., ge=2000, le=200000)
    center: LocationCenter


class LocationVerificationInsight(BaseModel):
    """Model for a location verification insight request.

    This insight verifies whether the device associated with the phone number
    is located within the specified geographic area.

    Args:
        location (Location): Geographic area used for verification.
    """

    location: Location


class InsightsRequest(BaseModel):
    """Model for a collection of identity insight requests.

    Each field represents an individual insight. Only the insights included
    in this object will be processed and returned in the response.

    Args:
        format (EmptyInsight, Optional): Request phone number format validation.
        sim_swap (SimSwapInsight, Optional): Request SIM swap information.
        original_carrier (EmptyInsight, Optional): Request original carrier
            information.
        current_carrier (EmptyInsight, Optional): Request current carrier
            information.
        subscriber_match (SubscriberMatchInsight, Optional): Request subscriber
            identity matching.
        roaming (EmptyInsight, Optional): Request roaming status information.
        reachability (EmptyInsight, Optional): Request device reachability
            information.
        location_verification (LocationVerificationInsight, Optional): Request
            location verification.
    """

    format: Optional[EmptyInsight] = None
    sim_swap: Optional[SimSwapInsight] = None
    original_carrier: Optional[EmptyInsight] = None
    current_carrier: Optional[EmptyInsight] = None
    subscriber_match: Optional[SubscriberMatchInsight] = None
    roaming: Optional[EmptyInsight] = None
    reachability: Optional[EmptyInsight] = None
    location_verification: Optional[LocationVerificationInsight] = None

    def at_least_one_insight(cls, values):
        """Validate that at least one insight is provided."""
        if not any(v is not None for v in values.values()):
            raise ValueError("At least one insight must be provided")
        return values


class IdentityInsightsRequest(BaseModel):
    """Model for an Identity Insights API request.

    This model represents a single aggregated request for one or more identity
    insights related to a phone number.

    Args:
        phone_number (PhoneNumber): The phone number to retrieve identity
            insights for.
        purpose (str, Optional): Purpose of the request. Required for insights
            that rely on the Network Registry.
        insights (InsightsRequest): Collection of requested insights.
    """

    phone_number: PhoneNumber
    purpose: Optional[str] = Field(
        None, description="Purpose of the request (required for some insights)"
    )
    insights: InsightsRequest
