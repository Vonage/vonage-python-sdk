import os.path
import re

import pytest


try:
    from urllib.parse import urlparse, parse_qs
except ImportError:
    from urlparse import urlparse, parse_qs

import responses


def request_body():
    return responses.calls[0].request.body


def request_query():
    return urlparse(responses.calls[0].request.url).query


def request_params():
    """ Obtain the query params, as a dict. """
    return parse_qs(request_query())


def request_headers():
    return responses.calls[0].request.headers


def request_user_agent():
    return responses.calls[0].request.headers["User-Agent"]


def request_authorization():
    return responses.calls[0].request.headers["Authorization"].decode("utf-8")


def request_content_type():
    return responses.calls[0].request.headers["Content-Type"]


def stub(method, url, fixture_path=None, status_code=200):
    body = load_fixture(fixture_path) if fixture_path else '{"key":"value"}'
    responses.add(
        method, url, body=body, status=status_code, content_type="application/json"
    )


def stub_bytes(method, url):
    responses.add(method, url, body=b"THISISANMP3", status=200)


def assert_re(pattern, string):
    __tracebackhide__ = True
    if not re.search(pattern, string):
        pytest.fail("Cannot find pattern {!r} in {!r}".format(pattern, string))


def assert_basic_auth():
    params = request_params()
    assert "api_key" not in params
    assert "api_secret" not in params
    assert (
        request_headers()["Authorization"]
        == "Basic bmV4bW8tYXBpLWtleTpuZXhtby1hcGktc2VjcmV0"
    )


def load_fixture(fixture_path):
    return open(os.path.join(os.path.dirname(__file__), "data", fixture_path)).read()
