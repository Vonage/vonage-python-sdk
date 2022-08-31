from util import *

session_id = '1_MX4yOWY3NjBmOC03Y2UxLTQ2YzktYWRlMy1mMmRlZGVlNGVkNWZ-fjE2NjAwNjE0MTczMDJ-QmlCNzN1SVE2TVV2YUVFUHdIVUJHNFE1fn4'
connection_id = '1234-5678'

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
    stream_id = 'my_stream_id'
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
