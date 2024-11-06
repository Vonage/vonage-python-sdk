from typing import Optional

from pydantic import BaseModel, Field


class Balance(BaseModel):
    """Model for the balance of a Vonage account.

    Args:
        value (float): The balance of the account in EUR.
        auto_reload (bool, Optional): Whether the account has auto-reload enabled.
    """

    value: float
    auto_reload: Optional[bool] = Field(None, validation_alias='autoReload')


class TopUpResponse(BaseModel):
    """Model for a response to a top-up request.

    Args:
        error_code (str, Optional): Code describing the operation status.
        error_code_label (str, Optional): Description of the operation status.
    """

    error_code: Optional[str] = Field(None, validation_alias='error-code')
    error_code_label: Optional[str] = Field(None, validation_alias='error-code-label')


class SettingsResponse(BaseModel):
    """Model for a response to a settings update request.

    Args:
        mo_callback_url (str, Optional): The URL for the inbound SMS webhook.
        dr_callback_url (str, Optional): The URL for the delivery receipt webhook.
        max_outbound_request (int, Optional): The maximum number of outbound messages
            per second.
        max_inbound_request (int, Optional): The maximum number of inbound messages
            per second.
        max_calls_per_second (int, Optional): The maximum number of API calls per second.
    """

    mo_callback_url: Optional[str] = Field(None, validation_alias='mo-callback-url')
    dr_callback_url: Optional[str] = Field(None, validation_alias='dr-callback-url')
    max_outbound_request: Optional[int] = Field(
        None, validation_alias='max-outbound-request'
    )
    max_inbound_request: Optional[int] = Field(
        None, validation_alias='max-inbound-request'
    )
    max_calls_per_second: Optional[int] = Field(
        None, validation_alias='max-calls-per-second'
    )


class NetworkPricing(BaseModel):
    """Model for network pricing data.

    Args:
        aliases (list[str], Optional): A list of aliases for the network.
        currency (str, Optional): The currency code for the pricing data.
        mcc (str, Optional): The mobile country code.
        mnc (str, Optional): The mobile network code.
        network_code (str, Optional): The network code.
        network_name (str, Optional): The network name.
        price (str, Optional): The price for the service.
        type (str, Optional): The type of service.
        ranges (str, Optional): Number ranges.
    """

    aliases: Optional[list[str]] = None
    currency: Optional[str] = None
    mcc: Optional[str] = None
    mnc: Optional[str] = None
    network_code: Optional[str] = Field(None, validation_alias='networkCode')
    network_name: Optional[str] = Field(None, validation_alias='networkName')
    price: Optional[str] = None
    type: Optional[str] = None
    ranges: Optional[list[int]] = None


class GetPricingResponse(BaseModel):
    """Model for a response to a request for pricing data.

    Args:
        country_code (str, Optional): The two-letter country code.
        country_display_name (str, Optional): The display name of the country.
        country_name (str, Optional): The name of the country.
        currency (str, Optional): The currency code for the pricing data.
        default_price (str, Optional): The default price for the service.
        dialing_prefix (str, Optional): The dialing prefix for the country.
        networks (list[NetworkPricing], Optional): A list of network pricing data.
    """

    country_code: Optional[str] = Field(None, validation_alias='countryCode')
    country_display_name: Optional[str] = Field(
        None, validation_alias='countryDisplayName'
    )
    country_name: Optional[str] = Field(None, validation_alias='countryName')
    currency: Optional[str] = None
    default_price: Optional[str] = Field(None, validation_alias='defaultPrice')
    dialing_prefix: Optional[str] = Field(None, validation_alias='dialingPrefix')
    networks: Optional[list[NetworkPricing]] = None


class GetMultiplePricingResponse(BaseModel):
    """Model for multiple countries' pricing data.

    Args:
        count (int): The number of countries.
        countries (list[GetCountryPricingResponse]): A list of country pricing data.
    """

    count: int
    countries: list[GetPricingResponse]


class VonageApiSecret(BaseModel):
    """Model for a Vonage API secret.

    Args:
        id (str): The unique ID of the secret.
        created_at (str): The timestamp when the secret was created.
    """

    id: str
    created_at: str
