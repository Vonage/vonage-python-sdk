import vonage
from util import *


def test_check_signature(dummy_data):
    params = {
        "a": "1",
        "b": "2",
        "timestamp": "1461605396",
        "sig": "6af838ef94998832dbfc29020b564830",
    }

    client = vonage.Client(
        key=dummy_data.api_key, secret=dummy_data.api_secret, signature_secret="secret"
    )

    assert client.check_signature(params)


def test_signature(client, dummy_data):
    params = {"a": "1", "b": "2", "timestamp": "1461605396"}
    client = vonage.Client(
        key=dummy_data.api_key, secret=dummy_data.api_secret, signature_secret="secret"
    )
    assert client.signature(params) == "6af838ef94998832dbfc29020b564830"


def test_signature_adds_timestamp(dummy_data):
    params = {"a=7": "1", "b": "2 & 5"}

    client = vonage.Client(
        key=dummy_data.api_key, secret=dummy_data.api_secret, signature_secret="secret"
    )

    client.signature(params)
    assert params["timestamp"] is not None


def test_signature_md5(dummy_data):
    params = {"a": "1", "b": "2", "timestamp": "1461605396"}
    client = vonage.Client(
        key=dummy_data.api_key,
        secret=dummy_data.api_secret,
        signature_secret=dummy_data.signature_secret,
        signature_method="md5",
    )
    assert client.signature(params) == "c15c21ced558c93a226c305f58f902f2"


def test_signature_sha1(dummy_data):
    params = {"a": "1", "b": "2", "timestamp": "1461605396"}
    client = vonage.Client(
        key=dummy_data.api_key,
        secret=dummy_data.api_secret,
        signature_secret=dummy_data.signature_secret,
        signature_method="sha1",
    )
    assert client.signature(params) == "3e19a4e6880fdc2c1426bfd0587c98b9532f0210"


def test_signature_sha256(dummy_data):
    params = {"a": "1", "b": "2", "timestamp": "1461605396"}
    client = vonage.Client(
        key=dummy_data.api_key,
        secret=dummy_data.api_secret,
        signature_secret=dummy_data.signature_secret,
        signature_method="sha256",
    )
    assert (
        client.signature(params)
        == "a321e824b9b816be7c3f28859a31749a098713d39f613c80d455bbaffae1cd24"
    )


def test_signature_sha512(dummy_data):
    params = {"a": "1", "b": "2", "timestamp": "1461605396"}
    client = vonage.Client(
        key=dummy_data.api_key,
        secret=dummy_data.api_secret,
        signature_secret=dummy_data.signature_secret,
        signature_method="sha512",
    )
    assert (
        client.signature(params)
        == "812a18f76680fa0fe1b8bd9ee1625466ceb1bd96242e4d050d2cfd9a7b40166c63ed26ec9702168781b6edcf1633db8ff95af9341701004eec3fcf9550572ee8"
    )
