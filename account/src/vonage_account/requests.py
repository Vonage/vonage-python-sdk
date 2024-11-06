from enum import Enum

from pydantic import BaseModel


class ServiceType(str, Enum):
    """The service you wish to retrieve outbound pricing data about.

    Values:
    ```
    SMS: SMS
    SMS_TRANSIT: SMS transit
    VOICE: Voice
    ```
    """

    SMS = 'sms'
    SMS_TRANSIT = 'sms-transit'
    VOICE = 'voice'


class GetCountryPricingRequest(BaseModel):
    """The options for getting the pricing for a specific country.

    Args:
        country_code (str): The two-letter country code for the country to retrieve
            pricing data about.
        type (ServiceType, Optional): The type of service to retrieve pricing data about.
    """

    country_code: str
    type: ServiceType = ServiceType.SMS


class GetPrefixPricingRequest(BaseModel):
    """The options for getting the pricing for a specific prefix.

    Args:
        prefix (str): The numerical dialing prefix to look up pricing for, e.g. "1", "44".
        type (ServiceType, Optional): The type of service to retrieve pricing data about.
    """

    prefix: str
    type: ServiceType = ServiceType.SMS
