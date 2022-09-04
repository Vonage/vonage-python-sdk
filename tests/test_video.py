from util import *

session_id = 'my_session_id'
stream_id = 'my_stream_id'
connection_id = '1234-5678'
archive_id = '1234-abcd'

@responses.activate
def test_create_session(client, dummy_data):
    stub(responses.POST, 
        "https://video.api.vonage.com/session/create", 
        fixture_path="video/create_session.json",
    )
    
    session = client.video.create_session()
    assert isinstance(session, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert session['session_id'] == session_id


@responses.activate
def test_get_stream(client, dummy_data):
    stub(responses.GET,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/stream/{stream_id}",
        fixture_path="video/get_stream.json"
    )

    stream = client.video.get_stream(session_id, stream_id)
    assert isinstance(stream, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert stream['videoType'] == 'camera'


@responses.activate
def test_list_streams(client, dummy_data):
    stub(responses.GET,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/stream",
        fixture_path="video/list_streams.json"
    )

    stream_list = client.video.list_streams(session_id)
    assert isinstance(stream_list, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert stream_list['items'][0]['videoType'] == 'camera'


@responses.activate
def test_change_stream_layout(client, dummy_data):
    stub(responses.PUT,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/stream"
    )

    items = [{
        'id': 'stream-1234', 
        'layoutClassList': ["full"]
    }]

    assert isinstance(client.video.set_stream_layout(session_id, items), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"


@responses.activate
def test_send_signal_to_all_participants(client, dummy_data):
    stub(responses.POST,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/signal"
    )

    assert isinstance(client.video.send_signal(session_id, type='chat', data='hello from a test case'), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"


@responses.activate
def test_send_signal_to_single_participant(client, dummy_data):
    stub(responses.POST,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/connection/{connection_id}/signal"
    )

    assert isinstance(client.video.send_signal(session_id, type='chat', data='hello from a test case', connection_id=connection_id), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"

@responses.activate
def test_disconnect_client(client, dummy_data):
    stub(responses.DELETE,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/connection/{connection_id}"
    )

    assert isinstance(client.video.disconnect_client(session_id, connection_id=connection_id), dict)
    assert request_user_agent() == dummy_data.user_agent

@responses.activate
def test_mute_specific_stream(client, dummy_data):
    stub(responses.POST,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/stream/{stream_id}/mute",
        fixture_path="video/mute_specific_stream.json"
    )

    response = client.video.mute_stream(session_id, stream_id)
    assert isinstance(response, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert response['createdAt'] == 1414642898000


@responses.activate
def test_mute_all_streams_except_excluded_list(client, dummy_data):
    stub(responses.POST,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/mute",
        fixture_path="video/mute_multiple_streams.json"
    )

    response = client.video.mute_all_streams(session_id, excluded_stream_ids=['excluded_stream_id_1', 'excluded_stream_id_2'])
    assert isinstance(response, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert response['createdAt'] == 1414642898000


@responses.activate
def test_list_archives_with_filters_applied(client, dummy_data):
    stub(responses.GET,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/archive",
        fixture_path="video/list_archives.json"
    )

    response = client.video.list_archives(offset=0, count=1, session_id=session_id)
    assert isinstance(response, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert response['items'][0]['createdAt'] == 1384221730000
    assert response['items'][0]['streams'][0]['streamId'] == 'abc123'


@responses.activate
def test_create_new_archive(client, dummy_data):
    stub(responses.POST,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/archive",
        fixture_path="video/create_archive.json"
    )

    response = client.video.create_archive(session_id=session_id, name='my_new_archive', outputMode='individual')
    assert isinstance(response, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert response['name'] == 'my_new_archive'
    assert response['createdAt'] == 1384221730555


@responses.activate
def test_get_archive(client, dummy_data):
    stub(responses.GET,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/archive/{archive_id}",
        fixture_path="video/get_archive.json"
    )

    response = client.video.get_archive(archive_id=archive_id)
    assert isinstance(response, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert response['duration'] == 5049
    assert response['size'] == 247748791
    assert response['streams'] == []


@responses.activate
def test_delete_archive(client, dummy_data):
    stub(responses.GET,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/archive/{archive_id}",
        status_code=204
    )

    assert client.video.delete_archive(archive_id=archive_id) == None
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_add_stream_to_archive(client, dummy_data):
    stub(responses.PATCH,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/archive/{archive_id}/streams",
        status_code=204
    )

    assert client.video.add_stream_to_archive(archive_id=archive_id, stream_id='1234', has_audio=True, has_video=True) == None
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_remove_stream_from_archive(client, dummy_data):
    stub(responses.PATCH,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/archive/{archive_id}/streams",
        status_code=204
    )

    assert client.video.remove_stream_from_archive(archive_id=archive_id, stream_id='1234') == None
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_stop_archive(client, dummy_data):
    stub(responses.POST,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/archive/{archive_id}/stop",
        fixture_path="video/stop_archive.json"
    )

    response = client.video.stop_archive(archive_id=archive_id)
    assert isinstance(response, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert response['name'] == 'my_new_archive'
    assert response['createdAt'] == 1384221730555
    assert response['status'] == 'stopped'


@responses.activate
def test_change_archive_layout(client, dummy_data):
    stub(responses.PUT,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/archive/{archive_id}/layout"
    )

    params = {
        'type': 'bestFit', 
        'screenshareType': 'horizontalPresentation'
    }

    assert isinstance(client.video.change_archive_layout(archive_id, params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert request_content_type() == "application/json"
