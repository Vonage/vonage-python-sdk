from vonage import Ncco
import json


action1 = Ncco.Action()
action2 = Ncco.Action()


def test_action_subclassing():
    assert issubclass(Ncco.Notify, Ncco.Action)


def test_can_build_ncco_from_abstract_actions():
    assert type(Ncco.build_ncco(action1, action2)) == str


def test_create_notify_action():
    notify = Ncco.Notify(payload={"message": "hello"}, eventUrl=["http://example.com"])
    assert type(notify) == Ncco.Notify
    assert (
        json.dumps(notify.dict())
        == '{"payload": {"message": "hello"}, "eventUrl": ["http://example.com"], "eventMethod": null, "action": "notify"}'
    )


def test_create_notify_action_with_optional_params():
    ...


def test_build_ncco_from_notify_actions():
    notify1 = Ncco.Notify(payload={"message": "hello"}, eventUrl=["http://example.com"])
    notify2 = Ncco.Notify(payload={"message": "world"}, eventUrl=["http://example.com"])
    ncco = Ncco.build_ncco(notify1, notify2)
    assert type(ncco) == str
