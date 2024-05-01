from enum import Enum


class Region(str, Enum):
    NA_EAST = 'na-east'
    NA_WEST = 'na-west'
    EU_EAST = 'eu-east'
    EU_WEST = 'eu-west'
    APAC_SNG = 'apac-sng'
    APAC_AUSTRALIA = 'apac-australia'
