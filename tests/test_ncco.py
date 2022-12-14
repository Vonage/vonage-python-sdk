from vonage.ncco import *


ncco_builder = NccoBuilder()
action1 = Action()
action2 = Action()


def test_can_create_action():
    assert type(ncco_builder.create_ncco_action(Action)) == Action


def test_can_build_actions():
    assert type(ncco_builder.build_ncco(action1, action2)) == list


def test_create_notify_action():
    ncco_builder.create_ncco_action(Notify, payload='asdf')