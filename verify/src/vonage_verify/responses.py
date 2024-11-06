from typing import Optional

from pydantic import BaseModel


class StartVerificationResponse(BaseModel):
    """Model for the response of a start verification request.

    Args:
        request_id (str): The request ID.
        check_url (str, Optional): URL for Silent Authentication Verify workflow
            completion (only shows if using Silent Auth).
    """

    request_id: str
    check_url: Optional[str] = None


class CheckCodeResponse(BaseModel):
    """Model for the response of a check code request.

    Args:
        request_id (str): The request ID.
        status (str): The status of the verification request.
    """

    request_id: str
    status: str
