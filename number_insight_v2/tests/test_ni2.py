import pytest


def test_raise_exception():
    with pytest.raises(Exception):
        raise Exception
    assert True
