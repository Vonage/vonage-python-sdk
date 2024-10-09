from enum import Enum


class Region(str, Enum):
    """All inbound, programmable SIP and SIP connect voice calls will be sent to the
    selected region unless the call itself is sent to a regional endpoint.

    If the call is using a regional endpoint, this will override the application setting.
    """

    NA_EAST = 'na-east'
    NA_WEST = 'na-west'
    EU_EAST = 'eu-east'
    EU_WEST = 'eu-west'
    APAC_SNG = 'apac-sng'
    APAC_AUSTRALIA = 'apac-australia'
