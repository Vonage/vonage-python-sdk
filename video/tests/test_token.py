from vonage_video.errors import TokenExpiryError
from vonage_video.models.token import TokenOptions
from vonage_video.models.enums import TokenRole
from vonage_video.video import Video

from vonage_http_client import HttpClient
from testutils import get_mock_jwt_auth

video = Video(HttpClient(get_mock_jwt_auth()))


def test_token_options_model():
    token_options = TokenOptions(
        session_id='session-id',
        scope='session.connect',
        role=TokenRole.PUBLISHER,
        connection_data='connection-data',
        initial_layout_class_list=['focus'],
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

    print(token)

    assert (
        token
        == b'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXNzaW9uX2lkIjoic2Vzc2lvbi1pZCIsInNjb3BlIjoic2Vzc2lvbi5jb25uZWN0Iiwicm9sZSI6InB1Ymxpc2hlciIsImNvbm5lY3Rpb25fZGF0YSI6ImNvbm5lY3Rpb24tZGF0YSIsImluaXRpYWxfbGF5b3V0X2NsYXNzX2xpc3QiOlsiZm9jdXMiXSwiZXhwIjoxMjM0NTc2ODksImp0aSI6IjRjYWI4OWNhLWI2MzctNDFjOC1iNjJmLTdiOWNlMTBjMzk3MSIsImlhdCI6MTIzNDU2Nzg5LCJzdWJqZWN0IjoidmlkZW8iLCJhY2wiOnsicGF0aHMiOnsiL3Nlc3Npb24vKioiOnt9fX0sImFwcGxpY2F0aW9uX2lkIjoidGVzdF9hcHBsaWNhdGlvbl9pZCJ9.NlAntZ_b1hUmcwOt62iI0R_AboscqA8I5ZaZpjQ9_fF0f0xwjfOJ9lVQJujLkR3lghLbYUJKi6gNOY4OvkcV57V0KDe5QMOH77lwRKI_F0H2hIlARR9EEhRTjqtjNzVPJdTOz99q3TyQ4F9CBreO4jLOqV1t4hlrwDou0cAnj6LmIYIItZFzRxlxX54E7l8SXOXS5xSAo3mNtmQ9WoxyZ1bNWSMLkpJ1MPmuOJSafPPbHu_-MyVHndlERVIY9vrebyc9qw8rNFuo04TuIJmcBCo2yTsMqHbaxQTvx569P-_FwBfQLF3maDO493mL63JvOd_xLAIU1xleK774SQTgEQ'
    )
