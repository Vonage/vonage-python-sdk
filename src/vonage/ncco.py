from pydantic import BaseModel, Field, constr, HttpUrl, validator, conset
from typing import Optional, List
from enum import Enum
import json


class HttpRequestEnum(str, Enum):
    get = 'GET'
    post = 'POST'
    put = 'PUT'
    update = 'UPDATE'
    delete = 'DELETE'


class Ncco:  # Used for namespacing reasons
    class Action(BaseModel):
        pass

    class Record(Action):
        ...

    class Conversation(Action):
        ...

    class Connect(Action):
        ...

    class Talk(Action):
        ...

    class Stream(Action):
        ...

    class Input(Action):
        ...

    class Notify(Action):
        """Use the notify action to send a custom payload to your event URL."""

        action = Field('notify', const=True)
        payload: dict
        eventUrl: List[HttpUrl]
        eventMethod: Optional[HttpRequestEnum]

        # @validator('eventMethod')
        # def check_valid_eventMethod(cls, v):
        #     if v != 'POST' or v != 'PUT':
        #         raise ValueError('Invalid eventMethod specified. Must be POST or PUT.')
        #     return v

    class Pay(Action):
        ...

    @staticmethod
    def build_ncco(*args: Action):
        ncco = []
        for action in args:
            ncco.append(action.dict())
        print(f'ncco is this: {ncco}')
        print(f'json representation is this: {json.dumps(ncco)}')
        return json.dumps(ncco)


class Message(BaseModel):
    to: constr(min_length=7, max_length=15)
    sender: constr(min_length=1)
    client_ref: Optional[str]


class SmsMessage(Message):
    channel = Field(default='sms', const=True)
    message_type = Field(default='text', const=True)
    text: constr(max_length=1000)


def send_message_from_model(self, message: Message):
    params = message.dict()
    params['from'] = params.pop('sender')

    print('params = ', params)

    if self._client.jwt is None:
        self._auth_type = 'header'
    return self._client.post(
        self._client.api_host(),
        "/v1/messages",
        params,
        auth_type=self._auth_type,
    )
