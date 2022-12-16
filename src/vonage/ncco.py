from pydantic import BaseModel, Field, HttpUrl, validator, constr, confloat
from typing import Optional, List, Union
from enum import Enum
from collections import OrderedDict
import json


class Ncco:  # Used for namespacing reasons
    class Action(BaseModel):
        ...

    class Record(Action):
        ...

    class Conversation(Action):
        ...

    class Connect(Action):
        ...

    class Talk(Action):
        """The talk action sends synthesized speech to a Conversation."""

        action = Field('talk', const=True)
        text = constr(max_length=1500)
        bargeIn: Optional[bool]
        loop: Optional[int]
        level: Optional[confloat(ge=-1, le=1)]
        language: Optional[str]
        style: Optional[int]
        premium: Optional[bool]

    class Stream(Action):
        ...

    class Input(Action):
        ...

    class Notify(Action):
        """Use the notify action to send a custom payload to your event URL."""

        action = Field('notify', const=True)
        payload: dict
        eventUrl: Union[List[HttpUrl], HttpUrl]
        eventMethod: Optional[constr(to_upper=True)]

        @validator('eventUrl')
        def check_url_in_list(cls, v):
            if type(v) != list:
                return [v]
            else:
                return v

    class Pay(Action):
        ...

    @staticmethod
    def build_ncco(*args: Action):
        ncco = []
        for action in args:
            ordered_action = OrderedDict(action.dict(exclude_none=True))
            ordered_action.move_to_end('action', last=False)
            ncco.append(ordered_action)
        print(f'ordered_ncco is this: {ncco}')
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
