from os.path import abspath

import responses
from pytest import raises
from vonage_application.application import Application
from vonage_application.common import (
    ApplicationUrl,
    Capabilities,
    Messages,
    MessagesWebhooks,
    Privacy,
    Rtc,
    RtcWebhooks,
    Vbc,
    Verify,
    VerifyWebhooks,
    Voice,
    VoiceUrl,
    VoiceWebhooks,
)
from vonage_application.enums import Region
from vonage_application.errors import ApplicationError
from vonage_application.requests import (
    ApplicationOptions,
    ListApplicationsFilter,
    RequestKeys,
)
from vonage_http_client.http_client import HttpClient

from testutils import build_response, get_mock_api_key_auth

path = abspath(__file__)

application = Application(HttpClient(get_mock_api_key_auth()))


def test_http_client_property():
    http_client = application.http_client
    assert isinstance(http_client, HttpClient)


@responses.activate
def test_create_application_basic():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/v2/applications',
        'create_application_basic.json',
    )
    app = application.create_application(ApplicationOptions(name='My Application'))

    assert app.id == 'ba1a6aa3-8ac6-487d-ac5c-be469e77ddb7'
    assert app.name == 'My Application'
    assert (
        app.keys.public_key
        == '-----BEGIN PUBLIC KEY-----\npublic_key_info_goes_here\n-----END PUBLIC KEY-----\n'
    )
    assert app.link == '/v2/applications/ba1a6aa3-8ac6-487d-ac5c-be469e77ddb7'


def test_create_application_options_model_from_dict():
    capabilities = {
        'voice': {
            'webhooks': {
                'answer_url': {
                    'address': 'https://example.com/answer',
                    'http_method': 'POST',
                    'connect_timeout': 500,
                    'socket_timeout': 3000,
                },
                'fallback_answer_url': {
                    'address': 'https://example.com/fallback',
                    'http_method': 'POST',
                    'connect_timeout': 500,
                    'socket_timeout': 3000,
                },
                'event_url': {
                    'address': 'https://example.com/event',
                    'http_method': 'POST',
                    'connect_timeout': 500,
                    'socket_timeout': 3000,
                },
            },
            'signed_callbacks': True,
            'conversations_ttl': 8000,
            'leg_persistence_time': 14,
            'region': 'na-east',
        },
        'rtc': {
            'webhooks': {
                'event_url': {
                    'address': 'https://example.com/event',
                    'http_method': 'POST',
                }
            },
            'signed_callbacks': True,
        },
        'messages': {
            'version': 'v1',
            'webhooks': {
                'inbound_url': {
                    'address': 'https://example.com/inbound',
                    'http_method': 'POST',
                },
                'status_url': {
                    'address': 'https://example.com/status',
                    'http_method': 'POST',
                },
            },
            'authenticate_inbound_media': True,
        },
        'verify': {
            'webhooks': {
                'status_url': {
                    'address': 'https://example.com/status',
                    'http_method': 'POST',
                }
            }
        },
        'vbc': {},
    }

    privacy = {'improve_ai': False}

    public_key = '-----BEGIN PUBLIC KEY-----\npublic_key_info_goes_here\n-----END PUBLIC KEY-----\n'
    keys = {'public_key': public_key}

    params = {
        'name': 'My Application Created from a Dict',
        'capabilities': capabilities,
        'privacy': privacy,
        'keys': keys,
    }
    application_options_dict = params
    application_options_model = ApplicationOptions(**application_options_dict)
    assert (
        application_options_model.model_dump(exclude_unset=True)
        == application_options_dict
    )


@responses.activate
def test_create_application_options_with_models():
    build_response(
        path,
        'POST',
        'https://api.nexmo.com/v2/applications',
        'create_application_options.json',
    )

    voice = Voice(
        webhooks=VoiceWebhooks(
            answer_url=VoiceUrl(
                address='https://example.com/answer',
                http_method='POST',
                connect_timeout=500,
                socket_timeout=3000,
            ),
            fallback_answer_url=VoiceUrl(
                address='https://example.com/fallback',
                http_method='POST',
                connect_timeout=500,
                socket_timeout=3000,
            ),
            event_url=VoiceUrl(
                address='https://example.com/event',
                http_method='POST',
                connect_timeout=500,
                socket_timeout=3000,
            ),
        ),
        signed_callbacks=True,
        conversations_ttl=8000,
        leg_persistence_time=14,
        region=Region.NA_EAST,
    )

    rtc = Rtc(
        webhooks=RtcWebhooks(
            event_url=ApplicationUrl(
                address='https://example.com/event', http_method='POST'
            ),
        ),
        signed_callbacks=True,
    )

    messages = Messages(
        version='v1',
        webhooks=MessagesWebhooks(
            inbound_url=ApplicationUrl(
                address='https://example.com/inbound', http_method='POST'
            ),
            status_url=ApplicationUrl(
                address='https://example.com/status', http_method='POST'
            ),
        ),
        authenticate_inbound_media=True,
    )

    verify = Verify(
        webhooks=VerifyWebhooks(
            status_url=ApplicationUrl(
                address='https://example.com/status', http_method='POST'
            )
        ),
    )

    capabilities = Capabilities(
        voice=voice, rtc=rtc, messages=messages, verify=verify, vbc=Vbc()
    )

    privacy = Privacy(improve_ai=False)

    public_key = '-----BEGIN PUBLIC KEY-----\npublic_key_info_goes_here\n-----END PUBLIC KEY-----\n'
    keys = RequestKeys(public_key=public_key)

    params = ApplicationOptions(
        name='My Customised Application',
        capabilities=capabilities,
        privacy=privacy,
        keys=keys,
    )
    app = application.create_application(params)

    assert app.id == '33e3329f-d1cc-48f3-9105-55e5a6e475c1'
    assert app.name == 'My Customised Application'
    assert app.keys.public_key == public_key
    assert app.link == '/v2/applications/33e3329f-d1cc-48f3-9105-55e5a6e475c1'
    assert app.privacy.improve_ai is False
    assert (
        app.capabilities.voice.webhooks.event_url.address == 'https://example.com/event'
    )
    assert app.capabilities.voice.webhooks.answer_url.socket_timeout == 3000
    assert app.capabilities.voice.webhooks.fallback_answer_url.connect_timeout == 500
    assert app.capabilities.voice.signed_callbacks is True
    assert app.capabilities.rtc.signed_callbacks is True
    assert app.capabilities.messages.version == 'v1'
    assert app.capabilities.messages.authenticate_inbound_media is True
    assert (
        app.capabilities.verify.webhooks.status_url.address
        == 'https://example.com/status'
    )
    assert app.capabilities.vbc.model_dump() == {}


def test_create_application_invalid_request_method():
    with raises(ApplicationError) as err:
        VerifyWebhooks(
            status_url=ApplicationUrl(
                address='https://example.com/status', http_method='GET'
            )
        )
    assert err.match('HTTP method must be POST')

    with raises(ApplicationError) as err:
        MessagesWebhooks(
            inbound_url=ApplicationUrl(
                address='https://example.com/inbound', http_method='GET'
            )
        )
    assert err.match('HTTP method must be POST')


@responses.activate
def test_list_applications_basic():
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/v2/applications',
        'list_applications_basic.json',
    )
    applications, next_page = application.list_applications()

    assert len(applications) == 1
    assert applications[0].id == '1b1b1b1b-1b1b-1b1b-1b1b-1b1b1b1b1b1b'
    assert applications[0].name == 'dev-application'
    assert (
        applications[0].keys.public_key
        == '-----BEGIN PUBLIC KEY-----\npublic_key_info_goes_here\n-----END PUBLIC KEY-----\n'
    )

    assert next_page is None


@responses.activate
def test_list_applications_multiple_pages():
    build_response(
        path,
        'GET',
        'https://api.nexmo.com/v2/applications',
        'list_applications_multiple_pages.json',
    )
    options = ListApplicationsFilter(page_size=3, page=1)
    applications, next_page = application.list_applications(options)

    assert len(applications) == 3
    assert applications[0].id == '1b1b1b1b-1b1b-1b1b-1b1b-1b1b1b1b1b1b'
    assert applications[0].name == 'dev-application'
    assert (
        applications[0].keys.public_key
        == '-----BEGIN PUBLIC KEY-----\npublic_key_info_goes_here\n-----END PUBLIC KEY-----\n'
    )
    assert applications[1].id == '2b2b2b2b-2b2b-2b2b-2b2b-2b2b2b2b2b2b'
    assert (
        applications[1].capabilities.voice.webhooks.event_url.address
        == 'http://9ff8266be1ed.ngrok.app/webhooks/events'
    )
    assert applications[2].id == '3b3b3b3b-3b3b-3b3b-3b3b-3b3b3b3b3b3b'
    assert next_page == 2
