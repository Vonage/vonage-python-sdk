from multiprocessing import dummy
from util import *

session_id = '1_MX4yOWY3NjBmOC03Y2UxLTQ2YzktYWRlMy1mMmRlZGVlNGVkNWZ-fjE2NjAwNjE0MTczMDJ-QmlCNzN1SVE2TVV2YUVFUHdIVUJHNFE1fn4'

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

