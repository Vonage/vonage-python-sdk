from util import *


@responses.activate
def test_get(client, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/v1/applications")
    host = "api.nexmo.com"
    request_uri = "/v1/applications"
    params = {"aaa": "xxx", "bbb": "yyy"}
    response = client.get(host, request_uri, params=params)
    assert isinstance(response, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "aaa=xxx" in request_query()
    assert "bbb=yyy" in request_query()


@responses.activate
def test_get_with_auth(client, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/v1/applications")
    host = "api.nexmo.com"
    request_uri = "/v1/applications"
    params = {"aaa": "xxx", "bbb": "yyy"}
    response = client.get(host, request_uri, params=params, header_auth=True)
    assert isinstance(response, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "aaa=xxx" in request_query()
    assert "bbb=yyy" in request_query()
    assert_basic_auth()


@responses.activate
def test_post(client, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/v1/applications")
    host = "api.nexmo.com"
    request_uri = "/v1/applications"
    params = {"aaa": "xxx", "bbb": "yyy"}
    response = client.post(host, request_uri, params)
    assert isinstance(response, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "aaa=xxx" in request_body()
    assert "bbb=yyy" in request_body()


@responses.activate
def test_post_with_auth(client, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/v1/applications")
    host = "api.nexmo.com"
    request_uri = "/v1/applications"
    params = {"aaa": "xxx", "bbb": "yyy"}
    response = client.post(host, request_uri, params, header_auth=True)
    assert isinstance(response, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "aaa=xxx" in request_body()
    assert "bbb=yyy" in request_body()
    assert_basic_auth()


@responses.activate
def test_put(client, dummy_data):
    stub(responses.PUT, "https://api.nexmo.com/v1/applications")
    host = "api.nexmo.com"
    request_uri = "/v1/applications"
    params = {"aaa": "xxx", "bbb": "yyy"}
    response = client.put(host, request_uri, params=params)
    assert isinstance(response, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert b"aaa" in request_body()
    assert b"xxx" in request_body()
    assert b"bbb" in request_body()
    assert b"yyy" in request_body()


@responses.activate
def test_put_with_auth(client, dummy_data):
    stub(responses.PUT, "https://api.nexmo.com/v1/applications")
    host = "api.nexmo.com"
    request_uri = "/v1/applications"
    params = {"aaa": "xxx", "bbb": "yyy"}
    response = client.put(host, request_uri, params=params, header_auth=True)
    assert_basic_auth()
    assert isinstance(response, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert b"aaa" in request_body()
    assert b"xxx" in request_body()
    assert b"bbb" in request_body()
    assert b"yyy" in request_body()


@responses.activate
def test_delete(client, dummy_data):
    stub(responses.DELETE, "https://api.nexmo.com/v1/applications")
    host = "api.nexmo.com"
    request_uri = "/v1/applications"
    response = client.delete(host, request_uri)
    assert isinstance(response, dict)
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_delete_with_auth(client, dummy_data):
    stub(responses.DELETE, "https://api.nexmo.com/v1/applications")
    host = "api.nexmo.com"
    request_uri = "/v1/applications"
    response = client.delete(host, request_uri, header_auth=True)
    assert isinstance(response, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert_basic_auth()
