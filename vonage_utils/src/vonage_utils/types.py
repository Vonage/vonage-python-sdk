from typing import Annotated

from pydantic import Field

PhoneNumber = Annotated[str, Field(pattern=r'^[1-9]\d{6,14}$')]
Dtmf = Annotated[str, Field(pattern=r'^[0-9#*p]+$')]
SipUri = Annotated[str, Field(pattern=r'^(sip|sips):\+?([\w|:.\-@;,=%&]+)')]
