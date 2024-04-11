from pydantic import BaseModel


class CreateCallResponse(BaseModel):
    uuid: str
    status: str
    direction: str
    conversation_uuid: str


class CallStatus(BaseModel):
    message: str
    uuid: str
