from .client import *
from .ncco_builder.ncco import *

__version__ = "3.18.0"

from warnings import warn

warn(
    'v3 of the Vonage Python SDK is now deprecated. Please upgrade to vonage>=4.0.0.',
    DeprecationWarning,
    stacklevel=2,
)
