import json

from vonage import Ncco
import ncco_samples.ncco_builder_samples as nbs


def test_build_basic_ncco():
    ncco = Ncco.build_ncco(nbs.talk_minimal)
    assert ncco == nbs.basic_ncco


def test_build_ncco_from_args():
    ncco = Ncco.build_ncco(nbs.record, nbs.talk_minimal)
    assert ncco == nbs.two_part_ncco
    assert (
        json.dumps(ncco)
        == '[{"action": "record", "eventUrl": ["http://example.com/events"]}, {"action": "talk", "text": "hello"}]'
    )


def test_build_ncco_from_list():
    action_list = [nbs.record, nbs.connect_advancedMachineDetection, nbs.talk_minimal]
    ncco = Ncco.build_ncco(actions=action_list)
    assert ncco == nbs.three_part_advancedMachineDetection_ncco


def test_build_insane_ncco():
    action_list = [
        nbs.record,
        nbs.conversation,
        nbs.connect,
        nbs.talk,
        nbs.stream,
        nbs.input,
        nbs.notify,
        nbs.pay_voice_prompt,
        nbs.pay_text_prompt,
    ]
    ncco = Ncco.build_ncco(actions=action_list)
    assert ncco == nbs.insane_ncco
