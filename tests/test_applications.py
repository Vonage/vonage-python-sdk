from util import *


@responses.activate
def test_get_applications(client, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/v1/applications")

    assert isinstance(client.get_applications(), dict)
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_get_application(client, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/v1/applications/xx-xx-xx-xx")

    assert isinstance(client.get_application("xx-xx-xx-xx"), dict)
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_create_application(client, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/v1/applications")

    params = {"name": "Example App", "type": "voice"}

    assert isinstance(client.create_application(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "name=Example+App" in request_body()
    assert "type=voice" in request_body()


@responses.activate
def test_update_application(client, dummy_data):
    stub(responses.PUT, "https://api.nexmo.com/v1/applications/xx-xx-xx-xx")

    params = {"answer_url": "https://example.com/ncco"}

    assert isinstance(client.update_application("xx-xx-xx-xx", params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"
    assert b'"answer_url": "https://example.com/ncco"' in request_body()


@responses.activate
def test_delete_application(client, dummy_data):
    responses.add(
        responses.DELETE,
        "https://api.nexmo.com/v1/applications/xx-xx-xx-xx",
        status=204,
    )

    assert client.delete_application("xx-xx-xx-xx") is None
    assert request_user_agent() == dummy_data.user_agent
