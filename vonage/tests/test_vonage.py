from vonage_http_client.http_client import HttpClient

from vonage.vonage import Auth, Vonage, __version__


def test_create_vonage_class_instance():
    vonage = Vonage(Auth(api_key='asdf', api_secret='qwerasdf'))

    assert vonage.http_client.auth.api_key == 'asdf'
    assert vonage.http_client.auth.api_secret == 'qwerasdf'
    assert (
        vonage.http_client.auth.create_basic_auth_string() == 'Basic YXNkZjpxd2VyYXNkZg=='
    )
    assert type(vonage.http_client) == HttpClient
    assert f'vonage-python-sdk/{__version__}' in vonage.http_client._user_agent
