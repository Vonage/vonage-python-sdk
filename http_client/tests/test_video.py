from util import *
from vonage import Client
from vonage.errors import (
    ClientError,
    VideoError,
    InvalidRoleError,
    TokenExpiryError,
    SipError,
)

import jwt
from time import time


session_id = 'my_session_id'
stream_id = 'my_stream_id'
connection_id = '1234-5678'
archive_id = '1234-abcd'
broadcast_id = '1748b7070a81464c9759c46ad10d3734'


@responses.activate
def test_create_default_session(client: Client, dummy_data):
    stub(
        responses.POST,
        "https://video.api.vonage.com/session/create",
        fixture_path="video/create_session.json",
    )

    session_info = client.video.create_session()
    assert isinstance(session_info, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert session_info['session_id'] == session_id
    assert session_info['archive_mode'] == 'manual'
    assert session_info['media_mode'] == 'routed'
    assert session_info['location'] == None


@responses.activate
def test_create_session_custom_archive_mode_and_location(client: Client):
    stub(
        responses.POST,
        "https://video.api.vonage.com/session/create",
        fixture_path="video/create_session.json",
    )

    session_options = {'archive_mode': 'always', 'location': '192.0.1.1', 'media_mode': 'routed'}
    session_info = client.video.create_session(session_options)
    assert isinstance(session_info, dict)
    assert session_info['session_id'] == session_id
    assert session_info['archive_mode'] == 'always'
    assert session_info['media_mode'] == 'routed'
    assert session_info['location'] == '192.0.1.1'


@responses.activate
def test_create_session_custom_media_mode(client: Client):
    stub(
        responses.POST,
        "https://video.api.vonage.com/session/create",
        fixture_path="video/create_session.json",
    )

    session_options = {'media_mode': 'relayed'}
    session_info = client.video.create_session(session_options)
    assert isinstance(session_info, dict)
    assert session_info['session_id'] == session_id
    assert session_info['archive_mode'] == 'manual'
    assert session_info['media_mode'] == 'relayed'
    assert session_info['location'] == None


def test_create_session_invalid_archive_mode(client: Client):
    session_options = {'archive_mode': 'invalid_option'}
    with pytest.raises(VideoError) as excinfo:
        client.video.create_session(session_options)
    assert 'Invalid archive_mode value. Must be one of ' in str(excinfo.value)


def test_create_session_invalid_media_mode(client: Client):
    session_options = {'media_mode': 'invalid_option'}
    with pytest.raises(VideoError) as excinfo:
        client.video.create_session(session_options)
    assert 'Invalid media_mode value. Must be one of ' in str(excinfo.value)


def test_create_session_invalid_mode_combination(client: Client):
    session_options = {'archive_mode': 'always', 'media_mode': 'relayed'}
    with pytest.raises(VideoError) as excinfo:
        client.video.create_session(session_options)
    assert (
        str(excinfo.value)
        == 'Invalid combination: cannot specify "archive_mode": "always" and "media_mode": "relayed".'
    )


def test_generate_client_token_all_defaults(client: Client):
    token = client.video.generate_client_token(session_id)
    decoded_token = jwt.decode(token, algorithms='RS256', options={'verify_signature': False})
    assert decoded_token['application_id'] == 'nexmo-application-id'
    assert decoded_token['scope'] == 'session.connect'
    assert decoded_token['session_id'] == 'my_session_id'
    assert decoded_token['role'] == 'publisher'
    assert decoded_token['initial_layout_class_list'] == ''


def test_generate_client_token_custom_options(client: Client):
    now = int(time())
    token_options = {
        'role': 'moderator',
        'data': 'some token data',
        'initialLayoutClassList': ['1234', '5678', '9123'],
        'expireTime': now + 60,
        'jti': 1234,
        'iat': now,
        'subject': 'test_subject',
        'acl': ['1', '2', '3'],
    }

    token = client.video.generate_client_token(session_id, token_options)
    decoded_token = jwt.decode(token, algorithms='RS256', options={'verify_signature': False})
    assert decoded_token['application_id'] == 'nexmo-application-id'
    assert decoded_token['scope'] == 'session.connect'
    assert decoded_token['session_id'] == 'my_session_id'
    assert decoded_token['role'] == 'moderator'
    assert decoded_token['initial_layout_class_list'] == ['1234', '5678', '9123']
    assert decoded_token['data'] == 'some token data'
    assert decoded_token['jti'] == 1234
    assert decoded_token['subject'] == 'test_subject'
    assert decoded_token['acl'] == ['1', '2', '3']


def test_check_client_token_headers(client: Client):
    token = client.video.generate_client_token(session_id)
    headers = jwt.get_unverified_header(token)
    assert headers['alg'] == 'RS256'
    assert headers['typ'] == 'JWT'


def test_generate_client_token_invalid_role(client: Client):
    with pytest.raises(InvalidRoleError):
        client.video.generate_client_token(session_id, {'role': 'observer'})


def test_generate_client_token_invalid_expire_time(client: Client):
    now = int(time())
    with pytest.raises(TokenExpiryError):
        client.video.generate_client_token(session_id, {'expireTime': now + 3600 * 24 * 30 + 1})


@responses.activate
def test_get_stream(client: Client):
    stub(
        responses.GET,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/stream/{stream_id}",
        fixture_path="video/get_stream.json",
    )

    stream = client.video.get_stream(session_id, stream_id)
    assert isinstance(stream, dict)
    assert stream['videoType'] == 'camera'


@responses.activate
def test_list_streams(
    client: Client,
):
    stub(
        responses.GET,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/stream",
        fixture_path="video/list_streams.json",
    )

    stream_list = client.video.list_streams(session_id)
    assert isinstance(stream_list, dict)
    assert stream_list['items'][0]['videoType'] == 'camera'


@responses.activate
def test_change_stream_layout(client: Client):
    stub(
        responses.PUT,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/stream",
    )

    items = [{'id': 'stream-1234', 'layoutClassList': ["full"]}]

    assert isinstance(client.video.set_stream_layout(session_id, items), dict)
    assert request_content_type() == "application/json"


@responses.activate
def test_send_signal_to_all_participants(client: Client):
    stub(
        responses.POST,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/signal",
    )

    assert isinstance(
        client.video.send_signal(session_id, type='chat', data='hello from a test case'), dict
    )
    assert request_content_type() == "application/json"


@responses.activate
def test_send_signal_to_single_participant(client: Client):
    stub(
        responses.POST,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/connection/{connection_id}/signal",
    )

    assert isinstance(
        client.video.send_signal(
            session_id, type='chat', data='hello from a test case', connection_id=connection_id
        ),
        dict,
    )
    assert request_content_type() == "application/json"


@responses.activate
def test_disconnect_client(client: Client):
    stub(
        responses.DELETE,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/connection/{connection_id}",
    )

    assert isinstance(client.video.disconnect_client(session_id, connection_id=connection_id), dict)


@responses.activate
def test_mute_specific_stream(client: Client):
    stub(
        responses.POST,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/stream/{stream_id}/mute",
        fixture_path="video/mute_specific_stream.json",
    )

    response = client.video.mute_stream(session_id, stream_id)
    assert isinstance(response, dict)
    assert response['createdAt'] == 1414642898000


@responses.activate
def test_mute_all_streams(client: Client):
    stub(
        responses.POST,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/mute",
        fixture_path="video/mute_multiple_streams.json",
    )

    response = client.video.mute_all_streams(session_id)
    assert isinstance(response, dict)
    assert response['createdAt'] == 1414642898000


@responses.activate
def test_mute_all_streams_except_excluded_list(client: Client):
    stub(
        responses.POST,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/mute",
        fixture_path="video/mute_multiple_streams.json",
    )

    response = client.video.mute_all_streams(
        session_id, excluded_stream_ids=['excluded_stream_id_1', 'excluded_stream_id_2']
    )
    assert isinstance(response, dict)
    assert response['createdAt'] == 1414642898000


@responses.activate
def test_disable_mute_all_streams(client: Client):
    stub(
        responses.POST,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/mute",
        fixture_path="video/disable_mute_multiple_streams.json",
    )

    response = client.video.disable_mute_all_streams(
        session_id, excluded_stream_ids=['excluded_stream_id_1', 'excluded_stream_id_2']
    )
    assert isinstance(response, dict)
    assert (
        request_body()
        == b'{"active": false, "excludedStreamIds": ["excluded_stream_id_1", "excluded_stream_id_2"]}'
    )
    assert response['createdAt'] == 1414642898000


@responses.activate
def test_list_archives_with_filters_applied(client: Client):
    stub(
        responses.GET,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/archive",
        fixture_path="video/list_archives.json",
    )

    response = client.video.list_archives(offset=0, count=1, session_id=session_id)
    assert isinstance(response, dict)
    assert response['items'][0]['createdAt'] == 1384221730000
    assert response['items'][0]['streams'][0]['streamId'] == 'abc123'


@responses.activate
def test_create_new_archive(client: Client):
    stub(
        responses.POST,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/archive",
        fixture_path="video/create_archive.json",
    )

    response = client.video.create_archive(
        session_id=session_id, name='my_new_archive', outputMode='individual'
    )
    assert isinstance(response, dict)
    assert response['name'] == 'my_new_archive'
    assert response['createdAt'] == 1384221730555


@responses.activate
def test_get_archive(client: Client):
    stub(
        responses.GET,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/archive/{archive_id}",
        fixture_path="video/get_archive.json",
    )

    response = client.video.get_archive(archive_id=archive_id)
    assert isinstance(response, dict)
    assert response['duration'] == 5049
    assert response['size'] == 247748791
    assert response['streams'] == []


@responses.activate
def test_delete_archive(client: Client):
    stub(
        responses.GET,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/archive/{archive_id}",
        status_code=204,
        fixture_path='no_content.json',
    )

    assert client.video.delete_archive(archive_id=archive_id) == None


@responses.activate
def test_add_stream_to_archive(client: Client):
    stub(
        responses.PATCH,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/archive/{archive_id}/streams",
        status_code=204,
        fixture_path='no_content.json',
    )

    assert (
        client.video.add_stream_to_archive(
            archive_id=archive_id, stream_id='1234', has_audio=True, has_video=True
        )
        == None
    )


@responses.activate
def test_remove_stream_from_archive(client: Client):
    stub(
        responses.PATCH,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/archive/{archive_id}/streams",
        status_code=204,
        fixture_path='no_content.json',
    )

    assert client.video.remove_stream_from_archive(archive_id=archive_id, stream_id='1234') == None


@responses.activate
def test_stop_archive(client: Client):
    stub(
        responses.POST,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/archive/{archive_id}/stop",
        fixture_path="video/stop_archive.json",
    )

    response = client.video.stop_archive(archive_id=archive_id)
    assert response['name'] == 'my_new_archive'
    assert response['createdAt'] == 1384221730555
    assert response['status'] == 'stopped'


@responses.activate
def test_change_archive_layout(client: Client):
    stub(
        responses.PUT,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/archive/{archive_id}/layout",
    )

    params = {'type': 'bestFit', 'screenshareType': 'horizontalPresentation'}

    assert isinstance(client.video.change_archive_layout(archive_id, params), dict)
    assert request_content_type() == "application/json"


@responses.activate
def test_create_sip_call(client):
    stub(
        responses.POST,
        f'https://video.api.vonage.com/v2/project/{client.application_id}/dial',
        fixture_path='video/create_sip_call.json',
    )

    sip = {'uri': 'sip:user@sip.partner.com;transport=tls'}

    sip_call = client.video.create_sip_call(session_id, 'my_token', sip)
    assert sip_call['id'] == 'b0a5a8c7-dc38-459f-a48d-a7f2008da853'
    assert sip_call['connectionId'] == 'e9f8c166-6c67-440d-994a-04fb6dfed007'
    assert sip_call['streamId'] == '482bce73-f882-40fd-8ca5-cb74ff416036'


@responses.activate
def test_create_sip_call_not_found_error(client):
    stub(
        responses.POST,
        f'https://video.api.vonage.com/v2/project/{client.application_id}/dial',
        status_code=404,
    )
    sip = {'uri': 'sip:user@sip.partner.com;transport=tls'}
    with pytest.raises(ClientError):
        client.video.create_sip_call('an-invalid-session-id', 'my_token', sip)


def test_create_sip_call_no_uri_error(client):
    sip = {}
    with pytest.raises(SipError) as err:
        client.video.create_sip_call(session_id, 'my_token', sip)

    assert str(err.value) == 'You must specify a uri when creating a SIP call.'


@responses.activate
def test_play_dtmf(client):
    stub(
        responses.POST,
        f'https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/play-dtmf',
        fixture_path='no_content.json',
    )

    assert client.video.play_dtmf(session_id, '1234') == None


@responses.activate
def test_play_dtmf_specific_connection(client):
    stub(
        responses.POST,
        f'https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/connection/my-connection-id/play-dtmf',
        fixture_path='no_content.json',
    )

    assert client.video.play_dtmf(session_id, '1234', connection_id='my-connection-id') == None


@responses.activate
def test_play_dtmf_invalid_session_id_error(client):
    stub(
        responses.POST,
        f'https://video.api.vonage.com/v2/project/{client.application_id}/session/{session_id}/play-dtmf',
        fixture_path='video/play_dtmf_invalid_error.json',
        status_code=400,
    )

    with pytest.raises(ClientError) as err:
        client.video.play_dtmf(session_id, '1234')
    assert 'One of the properties digits or sessionId is invalid.' in str(err.value)


def test_play_dtmf_invalid_input_error(client):
    with pytest.raises(VideoError) as err:
        client.video.play_dtmf(session_id, '!@£$%^&()asdfghjkl;')

    assert str(err.value) == 'Only digits 0-9, *, #, and "p" are allowed.'


@responses.activate
def test_list_broadcasts(client):
    stub(
        responses.GET,
        f'https://video.api.vonage.com/v2/project/{client.application_id}/broadcast',
        fixture_path='video/list_broadcasts.json',
    )

    broadcasts = client.video.list_broadcasts()
    assert broadcasts['count'] == '1'
    assert broadcasts['items'][0]['id'] == '1748b7070a81464c9759c46ad10d3734'
    assert broadcasts['items'][0]['applicationId'] == 'abc123'


@responses.activate
def test_list_broadcasts_options(client):
    stub(
        responses.GET,
        f'https://video.api.vonage.com/v2/project/{client.application_id}/broadcast',
        fixture_path='video/list_broadcasts.json',
    )

    broadcasts = client.video.list_broadcasts(
        count=1, session_id='2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4'
    )
    assert broadcasts['count'] == '1'
    assert broadcasts['items'][0]['sessionId'] == '2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4'
    assert broadcasts['items'][0]['id'] == '1748b7070a81464c9759c46ad10d3734'
    assert broadcasts['items'][0]['applicationId'] == 'abc123'


@responses.activate
def test_list_broadcasts_invalid_options_errors(client):
    stub(
        responses.GET,
        f'https://video.api.vonage.com/v2/project/{client.application_id}/broadcast',
        fixture_path='video/list_broadcasts.json',
    )

    with pytest.raises(VideoError) as err:
        client.video.list_broadcasts(offset=-2, session_id='2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4')
    assert str(err.value) == 'Offset must be an int >= 0.'

    with pytest.raises(VideoError) as err:
        client.video.list_broadcasts(count=9999, session_id='2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4')
    assert str(err.value) == 'Count must be an int between 0 and 1000.'

    with pytest.raises(VideoError) as err:
        client.video.list_broadcasts(offset='10', session_id='2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4')
    assert str(err.value) == 'Offset must be an int >= 0.'


@responses.activate
def test_start_broadcast_required_params(client):
    stub(
        responses.POST,
        f'https://video.api.vonage.com/v2/project/{client.application_id}/broadcast',
        fixture_path='video/broadcast.json',
    )

    params = {
        "sessionId": "2_MX40NTMyODc3Mn5-fg",
        "outputs": {
            "rtmp": [
                {
                    "id": "foo",
                    "serverUrl": "rtmps://myfooserver/myfooapp",
                    "streamName": "myfoostream",
                }
            ]
        },
    }

    broadcast = client.video.start_broadcast(params)
    assert broadcast['id'] == '1748b7070a81464c9759c46ad10d3734'
    assert broadcast['createdAt'] == 1437676551000
    assert broadcast['maxBitrate'] == 2000000
    assert broadcast['broadcastUrls']['rtmp'][0]['id'] == 'abc123'


@responses.activate
def test_start_broadcast_all_params(client):
    stub(
        responses.POST,
        f'https://video.api.vonage.com/v2/project/{client.application_id}/broadcast',
        fixture_path='video/broadcast.json',
    )

    params = {
        "sessionId": "2_MX40NTMyODc3Mn5-fg",
        "layout": {
            "type": "custom",
            "stylesheet": "the layout stylesheet (only used with type == custom)",
            "screenshareType": "horizontalPresentation",
        },
        "maxDuration": 5400,
        "outputs": {
            "rtmp": [
                {
                    "id": "foo",
                    "serverUrl": "rtmps://myfooserver/myfooapp",
                    "streamName": "myfoostream",
                }
            ]
        },
        "resolution": "1920x1080",
        "streamMode": "manual",
        "multiBroadcastTag": "foo",
    }

    broadcast = client.video.start_broadcast(params)
    assert broadcast['id'] == '1748b7070a81464c9759c46ad10d3734'
    assert broadcast['createdAt'] == 1437676551000
    assert broadcast['maxBitrate'] == 2000000
    assert broadcast['broadcastUrls']['rtmp'][0]['id'] == 'abc123'


@responses.activate
def test_get_broadcast(client):
    stub(
        responses.GET,
        f'https://video.api.vonage.com/v2/project/{client.application_id}/broadcast/{broadcast_id}',
        fixture_path='video/broadcast.json',
    )

    broadcast = client.video.get_broadcast(broadcast_id)
    assert broadcast['id'] == '1748b7070a81464c9759c46ad10d3734'
    assert broadcast['sessionId'] == '2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4'
    assert broadcast['updatedAt'] == 1437676551000
    assert broadcast['resolution'] == '640x480'


@responses.activate
def test_stop_broadcast(client):
    stub(
        responses.POST,
        f'https://video.api.vonage.com/v2/project/{client.application_id}/broadcast/{broadcast_id}',
        fixture_path='video/broadcast.json',
    )

    broadcast = client.video.stop_broadcast(broadcast_id)
    assert broadcast['id'] == '1748b7070a81464c9759c46ad10d3734'
    assert broadcast['sessionId'] == '2_MX4xMDBfjE0Mzc2NzY1NDgwMTJ-TjMzfn4'
    assert broadcast['updatedAt'] == 1437676551000
    assert broadcast['resolution'] == '640x480'


@responses.activate
def test_change_broadcast_layout(client):
    stub(
        responses.PUT,
        f'https://video.api.vonage.com/v2/project/{client.application_id}/broadcast/{broadcast_id}/layout',
        fixture_path='no_content.json',
    )

    params = {
        "type": "bestFit",
        "stylesheet": "stream.instructor {position: absolute; width: 100%;  height:50%;}",
        "screenshareType": "pip",
    }

    assert client.video.change_broadcast_layout(broadcast_id, params) == None


@responses.activate
def test_add_stream_to_broadcast(client: Client, dummy_data):
    stub(
        responses.PATCH,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/broadcast/{broadcast_id}/streams",
        status_code=204,
        fixture_path='no_content.json',
    )

    assert (
        client.video.add_stream_to_broadcast(
            broadcast_id=broadcast_id, stream_id='1234', has_audio=True, has_video=True
        )
        == None
    )
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_remove_stream_from_broadcast(client: Client, dummy_data):
    stub(
        responses.PATCH,
        f"https://video.api.vonage.com/v2/project/{client.application_id}/broadcast/{broadcast_id}/streams",
        status_code=204,
        fixture_path='no_content.json',
    )

    assert (
        client.video.remove_stream_from_broadcast(broadcast_id=broadcast_id, stream_id='1234')
        == None
    )
    assert request_user_agent() == dummy_data.user_agent
