from typing import Optional

from pydantic import BaseModel


class StartVerificationResponse(BaseModel):
    request_id: str
    check_url: Optional[str] = None


class CheckCodeResponse(BaseModel):
    request_id: str
    status: str
