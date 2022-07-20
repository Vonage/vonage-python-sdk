import json
from util import *

import vonage

@responses.activate
def test_deprecated_list_applications(application_v2, dummy_data):
    stub(
        responses.GET,
        "https://api.nexmo.com/v2/applications",
        fixture_path="applications/list_applications.json",
    )

    apps = application_v2.list_applications()
    assert_basic_auth()
    assert isinstance(apps, dict)
    assert apps["total_items"] == 30
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_deprecated_get_application(application_v2, dummy_data):
    stub(
        responses.GET,
        "https://api.nexmo.com/v2/applications/xx-xx-xx-xx",
        fixture_path="applications/get_application.json",
    )

    app = application_v2.get_application("xx-xx-xx-xx")
    assert_basic_auth()
    assert isinstance(app, dict)
    assert app["name"] == "My Test Application"
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_deprecated_create_application(application_v2, dummy_data):
    stub(
        responses.POST,
        "https://api.nexmo.com/v2/applications",
        fixture_path="applications/create_application.json",
    )

    params = {"name": "Example App", "type": "voice"}

    app = application_v2.create_application(params)
    assert_basic_auth()
    assert isinstance(app, dict)
    assert app["name"] == "My Test Application"
    assert request_user_agent() == dummy_data.user_agent
    body_data = json.loads(request_body().decode("utf-8"))
    assert body_data["type"] == "voice"


@responses.activate
def test_deprecated_update_application(application_v2, dummy_data):
    stub(
        responses.PUT,
        "https://api.nexmo.com/v2/applications/xx-xx-xx-xx",
        fixture_path="applications/update_application.json",
    )

    params = {"answer_url": "https://example.com/ncco"}

    app = application_v2.update_application("xx-xx-xx-xx", params)
    assert_basic_auth()
    assert isinstance(app, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"
    assert b'"answer_url": "https://example.com/ncco"' in request_body()

    assert app["name"] == "A Better Name"


@responses.activate
def test_deprecated_delete_application(application_v2, dummy_data):
    responses.add(
        responses.DELETE,
        "https://api.nexmo.com/v2/applications/xx-xx-xx-xx",
        status=204,
    )

    assert application_v2.delete_application("xx-xx-xx-xx") is None
    assert_basic_auth()
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_deprecated_authentication_error(application_v2):
    responses.add(
        responses.DELETE,
        "https://api.nexmo.com/v2/applications/xx-xx-xx-xx",
        status=401,
    )
    with pytest.raises(vonage.AuthenticationError):
        application_v2.delete_application("xx-xx-xx-xx")


@responses.activate
def test_deprecated_client_error(application_v2):
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
    with pytest.raises(vonage.ClientError) as exc_info:
        application_v2.delete_application("xx-xx-xx-xx")
    assert (
        str(exc_info.value) == "Nope: You really shouldn't have done that (nope_error)"
    )


@responses.activate
def test_deprecated_client_error_no_decode(application_v2):
    responses.add(
        responses.DELETE,
        "https://api.nexmo.com/v2/applications/xx-xx-xx-xx",
        status=430,
        body="{this: isnot_json",
    )
    with pytest.raises(vonage.ClientError) as exc_info:
        application_v2.delete_application("xx-xx-xx-xx")
    assert str(exc_info.value) == "430 response from api.nexmo.com"


@responses.activate
def test_deprecated_server_error(application_v2):
    responses.add(
        responses.DELETE,
        "https://api.nexmo.com/v2/applications/xx-xx-xx-xx",
        status=500,
    )
    with pytest.raises(vonage.ServerError):
        application_v2.delete_application("xx-xx-xx-xx")



@responses.activate
def test_list_applications(client, dummy_data):
    stub(
        responses.GET,
        "https://api.nexmo.com/v2/applications",
        fixture_path="applications/list_applications.json",
    )

    apps = client.application.list_applications()
    assert_basic_auth()
    assert isinstance(apps, dict)
    assert apps["total_items"] == 30
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_get_application(client, dummy_data):
    stub(
        responses.GET,
        "https://api.nexmo.com/v2/applications/xx-xx-xx-xx",
        fixture_path="applications/get_application.json",
    )

    app = client.application.get_application("xx-xx-xx-xx")
    assert_basic_auth()
    assert isinstance(app, dict)
    assert app["name"] == "My Test Application"
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_create_application(client, dummy_data):
    stub(
        responses.POST,
        "https://api.nexmo.com/v2/applications",
        fixture_path="applications/create_application.json",
    )

    params = {"name": "Example App", "type": "voice"}

    app = client.application.create_application(params)
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
        fixture_path="applications/update_application.json",
    )

    params = {"answer_url": "https://example.com/ncco"}

    app = client.application.update_application("xx-xx-xx-xx", params)
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

    assert client.application.delete_application("xx-xx-xx-xx") is None
    assert_basic_auth()
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_authentication_error(client):
    responses.add(
        responses.DELETE,
        "https://api.nexmo.com/v2/applications/xx-xx-xx-xx",
        status=401,
    )
    with pytest.raises(vonage.AuthenticationError):
        client.application.delete_application("xx-xx-xx-xx")


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
    with pytest.raises(vonage.ClientError) as exc_info:
        client.application.delete_application("xx-xx-xx-xx")
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
    with pytest.raises(vonage.ClientError) as exc_info:
        client.application.delete_application("xx-xx-xx-xx")
    assert str(exc_info.value) == "430 response from api.nexmo.com"


@responses.activate
def test_server_error(client):
    responses.add(
        responses.DELETE,
        "https://api.nexmo.com/v2/applications/xx-xx-xx-xx",
        status=500,
    )
    with pytest.raises(vonage.ServerError):
        client.application.delete_application("xx-xx-xx-xx")
