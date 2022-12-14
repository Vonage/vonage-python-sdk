from pydantic import BaseModel, Field, constr, HttpUrl
from typing import Optional, Sequence, Dict


class Action(BaseModel):
    test: Optional[Dict]


class Ncco(BaseModel):
    sections: Sequence[Action]


class NccoBuilder:
    def __init__(self):
        pass

    def create_ncco_action(self, action: Action, **kwargs):

        print(kwargs)
        return action(kwargs.values())
    
    def build_ncco(self, *args: Action):
        ncco = [] 
        for action in args:
            ncco.append(action.dict())
        print(ncco)
        return ncco





    

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
    payload: dict
    eventUrl: list[HttpUrl]

class Pay(Action):
    ...




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
        self._auth_type='header'
    return self._client.post(
        self._client.api_host(), 
        "/v1/messages",
        params,
        auth_type=self._auth_type,
    )