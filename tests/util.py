import re

import pytest

try:
    from urllib.parse import urlparse
except ImportError:
    from urlparse import urlparse

import responses


def request_body():
    return responses.calls[0].request.body


def request_query():
    return urlparse(responses.calls[0].request.url).query


def request_user_agent():
    return responses.calls[0].request.headers['User-Agent']


def request_authorization():
    return responses.calls[0].request.headers['Authorization'].decode('utf-8')


def request_content_type():
    return responses.calls[0].request.headers['Content-Type']


def stub(method, url):
    responses.add(method, url, body='{"key":"value"}', status=200, content_type='application/json')


def stub_bytes(method, url):
    responses.add(method, url, body=b'THISISANMP3', status=200)

def assert_re(pattern, string):
    __tracebackhide__ = True
    if not re.search(pattern, string):
        pytest.fail("Cannot find pattern %r in %r" % (pattern, string))
