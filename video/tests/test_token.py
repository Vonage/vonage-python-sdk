from time import time

from vonage_http_client import HttpClient
from vonage_video.errors import TokenExpiryError
from vonage_video.models.enums import TokenRole
from vonage_video.models.token import TokenOptions
from vonage_video.video import Video

from testutils import get_mock_jwt_auth

video = Video(HttpClient(get_mock_jwt_auth()))


def test_token_options_model():
    token_options = TokenOptions(
        session_id='session-id',
        scope='session.connect',
        role=TokenRole.PUBLISHER,
        connection_data='connection-data',
        initial_layout_class_list=['focus'],
        exp=int(time() + 15 * 60),
        jti='4cab89ca-b637-41c8-b62f-7b9ce10c3971',
        subject='video',
    )

    assert token_options.session_id == 'session-id'
    assert token_options.scope == 'session.connect'
    assert token_options.role == TokenRole.PUBLISHER
    assert token_options.connection_data == 'connection-data'
    assert token_options.initial_layout_class_list == ['focus']
    assert token_options.jti == '4cab89ca-b637-41c8-b62f-7b9ce10c3971'
    assert token_options.iat is not None
    assert token_options.subject == 'video'
    assert token_options.acl == {'paths': {'/session/**': {}}}


def test_token_options_invalid_expiry():
    try:
        TokenOptions(exp=0)
    except TokenExpiryError as e:
        assert str(e) == 'Token expiry date must be in the future.'

    try:
        TokenOptions(exp=99999999999)
    except TokenExpiryError as e:
        assert str(e) == 'Token expiry date must be less than 30 days from now.'


def test_generate_token():
    token = video.generate_client_token(
        TokenOptions(
            session_id='session-id',
            scope='session.connect',
            role=TokenRole.PUBLISHER,
            connection_data='connection-data',
            initial_layout_class_list=['focus'],
            jti='4cab89ca-b637-41c8-b62f-7b9ce10c3971',
            subject='video',
            iat=123456789,
        )
    )

    assert (
        token
        == b'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjoic2Vzc2lvbi1pZCIsInJvbGUiOiJwdWJsaXNoZXIiLCJjb25uZWN0aW9uX2RhdGEiOiJjb25uZWN0aW9uLWRhdGEiLCJpbml0aWFsX2xheW91dF9jbGFzc19saXN0IjpbImZvY3VzIl0sImV4cCI6MTIzNDU3Njg5LCJqdGkiOiI0Y2FiODljYS1iNjM3LTQxYzgtYjYyZi03YjljZTEwYzM5NzEiLCJpYXQiOjEyMzQ1Njc4OSwic3ViamVjdCI6InZpZGVvIiwic2NvcGUiOiJzZXNzaW9uLmNvbm5lY3QiLCJhY2wiOnsicGF0aHMiOnsiL3Nlc3Npb24vKioiOnt9fX0sImFwcGxpY2F0aW9uX2lkIjoidGVzdF9hcHBsaWNhdGlvbl9pZCJ9.DL-b9AJxZIKb0gmc_NGrD8fvIpg_ILX5FBMXpR56CgSdI63wS04VuaAKCTRojSJrqpzENv_GLR2HYY4-d1Qm1pyj1tM1yFRDk8z_vun30DWavYkCFW1T5FenK1VUjg0P9pbdGiPvq0Ku-taMuLyqXzQqHsbEGOovo-JMIag6wD6JPrPIKaYXsqGpXYaJ_BCcuIpg0NquQgJXA004Q415CxguCkQLdv0d7xTyfPw44Sj-_JfRdBdqDjyiDsmYmh7Yt5TrqRqZ1SwxNhNP7MSx8KDake3VqkQB9Iyys43MJBHZtRDrtE6VedLt80RpCz9Yo8F8CIjStwQPOfMjbV-iEA'
    )
