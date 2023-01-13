import pytest
import json

from vonage import Ncco
import ncco_samples.ncco_builder_samples as nbs


def test_build_basic_ncco():
    ncco = Ncco.build_ncco(nbs.talk_minimal)
    assert ncco == nbs.basic_ncco


def test_build_ncco_from_args():
    ncco = Ncco.build_ncco(nbs.record, nbs.talk_minimal)
    assert ncco == nbs.two_part_ncco
    assert json.dumps(ncco) == ''


def test_build_ncco_from_list():
    assert 0


def test_build_insane_ncco():
    ncco = Ncco.build_ncco(nbs.talk)
