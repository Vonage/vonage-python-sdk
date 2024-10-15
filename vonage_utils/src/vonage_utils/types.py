from typing import Annotated

from pydantic import Field

PhoneNumber = Annotated[str, Field(pattern=r'^[1-9]\d{6,14}$')]
"""A phone number, which must be between 7 and 15 digits long and not start with 0. Don't
use a leading `+` or `00` in the number. For example, use `447700900000` instead of
`+447700900000` or `00447700900000`.

Examples:
    - `447700900000`
    - `14155552671`
"""

Dtmf = Annotated[str, Field(pattern=r'^[0-9#*p]+$')]
"""A string of DTMF (Dual-Tone Multi-Frequency) tones. The string can contain the digits
0-9, the symbols `#`, `*`, and `p`. The `p` symbol represents a pause of 500ms.

Examples:
    - `1234#*`
    - `1p2p3p4`
"""

SipUri = Annotated[str, Field(pattern=r'^(sip|sips):\+?([\w|:.\-@;,=%&]+)')]
"""A SIP URI, which must start with `sip:` or `sips:` and contain a valid SIP address."""
