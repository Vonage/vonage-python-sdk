import json
from util import *

import nexmo


@responses.activate
def test_list_applications(client, dummy_data):
    stub(
        responses.GET,
        "https://api.nexmo.com/v2/applications",
        fixture_path="applications_v2/list_applications.json",
    )

    apps = client.application_v2.list_applications()
    assert_basic_auth()
    assert isinstance(apps, dict)
    assert apps["total_items"] == 30
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_get_application(client, dummy_data):
    stub(
        responses.GET,
        "https://api.nexmo.com/v2/applications/xx-xx-xx-xx",
        fixture_path="applications_v2/get_application.json",
    )

    app = client.application_v2.get_application("xx-xx-xx-xx")
    assert_basic_auth()
    assert isinstance(app, dict)
    assert app["name"] == "My Test Application"
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_create_application(client, dummy_data):
    stub(
        responses.POST,
        "https://api.nexmo.com/v2/applications",
        fixture_path="applications_v2/create_application.json",
    )

    params = {"name": "Example App", "type": "voice"}

    app = client.application_v2.create_application(params)
    assert_basic_auth()
    assert isinstance(app, dict)
    assert app["name"] == "My Test Application"
    assert request_user_agent() == dummy_data.user_agent
    body_data = json.loads(request_body().decode("utf-8"))
    assert body_data["type"] == "voice"


@responses.activate
def test_update_application(client, dummy_data):
    stub(
        responses.PUT,
        "https://api.nexmo.com/v2/applications/xx-xx-xx-xx",
        fixture_path="applications_v2/update_application.json",
    )

    params = {"answer_url": "https://example.com/ncco"}

    app = client.application_v2.update_application("xx-xx-xx-xx", params)
    assert_basic_auth()
    assert isinstance(app, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"
    assert b'"answer_url": "https://example.com/ncco"' in request_body()

    assert app["name"] == "A Better Name"


@responses.activate
def test_delete_application(client, dummy_data):
    responses.add(
        responses.DELETE,
        "https://api.nexmo.com/v2/applications/xx-xx-xx-xx",
        status=204,
    )

    assert client.application_v2.delete_application("xx-xx-xx-xx") is None
    assert_basic_auth()
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_authentication_error(client):
    responses.add(
        responses.DELETE,
        "https://api.nexmo.com/v2/applications/xx-xx-xx-xx",
        status=401,
    )
    with pytest.raises(nexmo.AuthenticationError):
        client.application_v2.delete_application("xx-xx-xx-xx")


@responses.activate
def test_client_error(client):
    responses.add(
        responses.DELETE,
        "https://api.nexmo.com/v2/applications/xx-xx-xx-xx",
        status=430,
        body=json.dumps(
            {
                "type": "nope_error",
                "title": "Nope",
                "detail": "You really shouldn't have done that",
            }
        ),
    )
    with pytest.raises(nexmo.ClientError) as exc_info:
        client.application_v2.delete_application("xx-xx-xx-xx")
    assert (
        str(exc_info.value) == "Nope: You really shouldn't have done that (nope_error)"
    )


@responses.activate
def test_client_error_no_decode(client):
    responses.add(
        responses.DELETE,
        "https://api.nexmo.com/v2/applications/xx-xx-xx-xx",
        status=430,
        body="{this: isnot_json",
    )
    with pytest.raises(nexmo.ClientError) as exc_info:
        client.application_v2.delete_application("xx-xx-xx-xx")
    assert str(exc_info.value) == "430 response"


@responses.activate
def test_server_error(client):
    responses.add(
        responses.DELETE,
        "https://api.nexmo.com/v2/applications/xx-xx-xx-xx",
        status=500,
    )
    with pytest.raises(nexmo.ServerError):
        client.application_v2.delete_application("xx-xx-xx-xx")


@responses.activate
def test_server_error(client):
    responses.add(
        responses.DELETE,
        "https://api.nexmo.com/v2/applications/xx-xx-xx-xx",
        status=500,
    )
    with pytest.raises(nexmo.ServerError):
        client.application_v2.delete_application("xx-xx-xx-xx")
