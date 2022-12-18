from vonage import Ncco
import data.ncco.ncco_action_samples as nas

import json
import pytest
from pydantic import ValidationError


def _action_as_dict(action: Ncco.Action):
    return action.dict(exclude_none=True)


def test_record_full():
    record = Ncco.Record(
        format='wav',
        split='conversation',
        channels=4,
        endOnSilence=5,
        endOnKey='*',
        timeOut=100,
        beepStart=True,
        eventUrl=['http://example.com'],
        eventMethod='PUT',
    )
    assert type(record) == Ncco.Record
    assert json.dumps(_action_as_dict(record)) == nas.record_full


def test_record_url_passed_as_str():
    record = Ncco.Record(eventUrl='http://example.com/events')
    assert json.dumps(_action_as_dict(record)) == nas.record_url_as_str


def test_record_channels_adds_split_parameter():
    record = Ncco.Record(channels=4)
    assert json.dumps(_action_as_dict(record)) == nas.record_add_split


def test_record_model_errors():
    with pytest.raises(ValidationError):
        Ncco.Record(format='mp4')
    with pytest.raises(ValidationError):
        Ncco.Record(endOnKey='asdf')


def test_conversation_basic():
    conversation = Ncco.Conversation(name='my_conversation')
    assert type(conversation) == Ncco.Conversation
    assert json.dumps(_action_as_dict(conversation)) == nas.conversation_basic


def test_conversation_full():
    conversation = Ncco.Conversation(
        name='my_conversation',
        musicOnHoldUrl='http://example.com/music.mp3',
        startOnEnter=True,
        endOnExit=True,
        record=True,
        canSpeak=['asdf', 'qwer'],
        canHear=['asdf'],
    )
    assert json.dumps(_action_as_dict(conversation)) == nas.conversation_full


def test_conversation_field_type_error():
    with pytest.raises(ValidationError):
        Ncco.Conversation(name='my_conversation', startOnEnter='asdf')


def test_conversation_mute():
    conversation = Ncco.Conversation(name='my_conversation', mute=True)
    assert json.dumps(_action_as_dict(conversation)) == nas.conversation_mute_option


def test_conversation_incompatible_options_error():
    with pytest.raises(ValidationError) as err:
        Ncco.Conversation(name='my_conversation', canSpeak=['asdf', 'qwer'], mute=True)
    str(err.value) == 'Cannot use mute option if canSpeak option is specified.+'


def test_connect_endpoint():
    connect = Ncco.Connect(from_='447000000000')
    print(connect.dict(exclude_none=False))
    connect = Ncco.Connect(endpoint={'phone'})


def test_talk_basic():
    talk = Ncco.Talk(text='hello')
    assert type(talk) == Ncco.Talk
    assert json.dumps(_action_as_dict(talk)) == nas.talk_basic


def test_talk_optional_params():
    talk = Ncco.Talk(text='hello', bargeIn=True, loop=3, level=0.5, language='en-GB', style=1, premium=True)
    assert json.dumps(_action_as_dict(talk)) == nas.talk_full


def test_talk_validation_error():
    with pytest.raises(ValidationError):
        Ncco.Talk(text='hello', bargeIn='go ahead')


def test_notify_basic():
    notify = Ncco.Notify(payload={"message": "hello"}, eventUrl=["http://example.com"])
    assert type(notify) == Ncco.Notify
    assert json.dumps(_action_as_dict(notify)) == nas.notify_basic


def test_notify_basic_str_in_event_url():
    notify = Ncco.Notify(payload={"message": "hello"}, eventUrl="http://example.com")
    assert type(notify) == Ncco.Notify
    assert json.dumps(_action_as_dict(notify)) == nas.notify_basic


def test_notify_full():
    notify = Ncco.Notify(payload={"message": "hello"}, eventUrl=["http://example.com"], eventMethod='POST')
    assert type(notify) == Ncco.Notify
    assert json.dumps(_action_as_dict(notify)) == nas.notify_full


def test_notify_validation_error():
    with pytest.raises(ValidationError):
        Ncco.Notify(payload={"message": "hello"}, eventUrl=["not-a-valid-url"])


def test_build_ncco_from_notify_actions():
    notify1 = Ncco.Notify(payload={"message": "hello"}, eventUrl=["http://example.com"])
    notify2 = Ncco.Notify(payload={"message": "world"}, eventUrl=["http://example.com"], eventMethod='PUT')
    ncco = Ncco.build_ncco(notify1, notify2)
    assert ncco == nas.two_notify_ncco
