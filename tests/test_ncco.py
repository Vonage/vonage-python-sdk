from vonage import Ncco
import data.ncco_samples as ns

import json
import pytest
from pydantic import ValidationError


def action_as_dict(action: Ncco.Action):
    return action.dict(exclude_none=True)


def test_basic_talk_action():
    talk = Ncco.Talk(text='hello')
    assert type(talk) == Ncco.Talk
    assert json.dumps(action_as_dict(talk)) == ns.basic_talk


def test_talk_action_optional_params():
    talk = Ncco.Talk(text='hello', bargeIn=True, loop=3, level=0.5, language='en-GB', style=1, premium=True)
    assert json.dumps(action_as_dict(talk)) == ns.full_talk


def test_talk_action_validation_error():
    with pytest.raises(ValidationError):
        Ncco.Talk(text='hello', bargeIn='go ahead')


def test_notify_action():
    notify = Ncco.Notify(payload={"message": "hello"}, eventUrl=["http://example.com"])
    assert type(notify) == Ncco.Notify
    assert json.dumps(action_as_dict(notify)) == ns.basic_notify


def test_notify_action_str_in_event_url():
    notify = Ncco.Notify(payload={"message": "hello"}, eventUrl="http://example.com")
    assert type(notify) == Ncco.Notify
    assert json.dumps(action_as_dict(notify)) == ns.basic_notify


def test_notify_action_with_optional_params():
    notify = Ncco.Notify(payload={"message": "hello"}, eventUrl=["http://example.com"], eventMethod='POST')
    assert type(notify) == Ncco.Notify
    assert json.dumps(action_as_dict(notify)) == ns.full_notify


def test_notify_validation_error():
    with pytest.raises(ValidationError):
        Ncco.Notify(payload={"message": "hello"}, eventUrl=["not-a-valid-url"])


def test_build_ncco_from_notify_actions():
    notify1 = Ncco.Notify(payload={"message": "hello"}, eventUrl=["http://example.com"])
    notify2 = Ncco.Notify(payload={"message": "world"}, eventUrl=["http://example.com"], eventMethod='PUT')
    ncco = Ncco.build_ncco(notify1, notify2)
    assert ncco == ns.two_notify_ncco
