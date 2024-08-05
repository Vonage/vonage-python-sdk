from os.path import abspath

import responses
from pytest import raises
from vonage_account.account import Account

# from vonage_account.errors import ApplicationError
# from vonage_account.requests import ApplicationConfig, ListApplicationsFilter
from vonage_http_client.http_client import HttpClient

from testutils import build_response, get_mock_api_key_auth

path = abspath(__file__)

account = Account(HttpClient(get_mock_api_key_auth()))


def test_http_client_property():
    http_client = account.http_client
    assert isinstance(http_client, HttpClient)


@responses.activate
def test_get_balance():
    build_response(
        path,
        'GET',
        'https://rest.nexmo.com/account/get-balance',
        'get_balance.json',
    )
    balance = account.get_balance()

    assert balance.value == 29.18202293
    assert balance.auto_reload is False


@responses.activate
def test_top_up():
    build_response(
        path,
        'POST',
        'https://rest.nexmo.com/account/top-up',
        'top_up.json',
    )
    top_up_response = account.top_up('1234567890')

    assert top_up_response.error_code == '200'
    assert top_up_response.error_code_label == 'success'


@responses.activate
def test_update_default_sms_webhook():
    build_response(
        path,
        'POST',
        'https://rest.nexmo.com/account/settings',
        'update_default_sms_webhook.json',
    )
    settings_response = account.update_default_sms_webhook(
        mo_callback_url='https://example.com/inbound_sms_webhook',
        dr_callback_url='https://example.com/delivery_receipt_webhook',
    )

    assert settings_response.mo_callback_url == 'https://example.com/inbound_sms_webhook'
    assert (
        settings_response.dr_callback_url
        == 'https://example.com/delivery_receipt_webhook'
    )
    assert settings_response.max_outbound_request == 30
    assert settings_response.max_inbound_request == 30
    assert settings_response.max_calls_per_second == 30


# def test_create_application_invalid_request_method():
#     with raises(ApplicationError) as err:
#         VerifyWebhooks(
#             status_url=ApplicationUrl(
#                 address='https://example.com/status', http_method='GET'
#             )
#         )
#     assert err.match('HTTP method must be POST')

#     with raises(ApplicationError) as err:
#         MessagesWebhooks(
#             inbound_url=ApplicationUrl(
#                 address='https://example.com/inbound', http_method='GET'
#             )
#         )
#     assert err.match('HTTP method must be POST')


# @responses.activate
# def test_list_applications_basic():
#     build_response(
#         path,
#         'GET',
#         'https://api.nexmo.com/v2/applications',
#         'list_applications_basic.json',
#     )
#     applications, next_page = application.list_applications()

#     assert len(applications) == 1
#     assert applications[0].id == '1b1b1b1b-1b1b-1b1b-1b1b-1b1b1b1b1b1b'
#     assert applications[0].name == 'dev-application'
#     assert (
#         applications[0].keys.public_key
#         == '-----BEGIN PUBLIC KEY-----\npublic_key_info_goes_here\n-----END PUBLIC KEY-----\n'
#     )

#     assert next_page is None


# @responses.activate
# def test_list_applications_multiple_pages():
#     build_response(
#         path,
#         'GET',
#         'https://api.nexmo.com/v2/applications',
#         'list_applications_multiple_pages.json',
#     )
#     options = ListApplicationsFilter(page_size=3, page=1)
#     applications, next_page = application.list_applications(options)

#     assert len(applications) == 3
#     assert applications[0].id == '1b1b1b1b-1b1b-1b1b-1b1b-1b1b1b1b1b1b'
#     assert applications[0].name == 'dev-application'
#     assert (
#         applications[0].keys.public_key
#         == '-----BEGIN PUBLIC KEY-----\npublic_key_info_goes_here\n-----END PUBLIC KEY-----\n'
#     )
#     assert applications[1].id == '2b2b2b2b-2b2b-2b2b-2b2b-2b2b2b2b2b2b'
#     assert (
#         applications[1].capabilities.voice.webhooks.event_url.address
#         == 'http://9ff8266be1ed.ngrok.app/webhooks/events'
#     )
#     assert applications[2].id == '3b3b3b3b-3b3b-3b3b-3b3b-3b3b3b3b3b3b'
#     assert next_page == 2


# @responses.activate
# def test_get_application():
#     build_response(
#         path,
#         'GET',
#         'https://api.nexmo.com/v2/applications/1b1b1b1b-1b1b-1b1b-1b1b-1b1b1b1b1b1b',
#         'get_application.json',
#     )
#     app = application.get_application('1b1b1b1b-1b1b-1b1b-1b1b-1b1b1b1b1b1b')

#     assert app.id == '1b1b1b1b-1b1b-1b1b-1b1b-1b1b1b1b1b1b'
#     assert app.link == '/v2/applications/1b1b1b1b-1b1b-1b1b-1b1b-1b1b1b1b1b1b'


# @responses.activate
# def test_update_application():
#     build_response(
#         path,
#         'PUT',
#         'https://api.nexmo.com/v2/applications/1b1b1b1b-1b1b-1b1b-1b1b-1b1b1b1b1b1b',
#         'update_application.json',
#     )

#     public_key = (
#         '-----BEGIN PUBLIC KEY-----\nupdated_public_key_info\n-----END PUBLIC KEY-----\n'
#     )
#     keys = Keys(public_key=public_key)
#     params = ApplicationConfig(name='My Updated Application', keys=keys)
#     application_data = application.update_application(
#         '1b1b1b1b-1b1b-1b1b-1b1b-1b1b1b1b1b1b', params
#     )

#     assert application_data.name == 'My Updated Application'
#     assert application_data.keys.public_key == public_key
#     assert (
#         application_data.link == '/v2/applications/1b1b1b1b-1b1b-1b1b-1b1b-1b1b1b1b1b1b'
#     )


# @responses.activate
# def test_delete_application():
#     responses.add(
#         responses.DELETE,
#         'https://api.nexmo.com/v2/applications/1b1b1b1b-1b1b-1b1b-1b1b-1b1b1b1b1b1b',
#         status=204,
#     )

#     application.delete_application('1b1b1b1b-1b1b-1b1b-1b1b-1b1b1b1b1b1b')
#     assert application.http_client.last_response.status_code == 204
