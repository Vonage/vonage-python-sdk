# from os.path import abspath

# import responses
# from pytest import raises
# from vonage_account.account import Account
# from vonage_account.errors import InvalidSecretError
# from vonage_http_client.errors import ForbiddenError
# from vonage_http_client.http_client import HttpClient

# from testutils import build_response, get_mock_api_key_auth

# path = abspath(__file__)

# account = Account(HttpClient(get_mock_api_key_auth()))


# def test_http_client_property():
#     http_client = account.http_client
#     assert isinstance(http_client, HttpClient)


# @responses.activate
# def test_get_balance():
#     build_response(
#         path,
#         'GET',
#         'https://rest.nexmo.com/account/get-balance',
#         'get_balance.json',
#     )
#     balance = account.get_balance()

#     assert balance.value == 29.18202293
#     assert balance.auto_reload is False


# @responses.activate
# def test_top_up():
#     build_response(
#         path,
#         'POST',
#         'https://rest.nexmo.com/account/top-up',
#         'top_up.json',
#     )
#     top_up_response = account.top_up('1234567890')

#     assert top_up_response.error_code == '200'
#     assert top_up_response.error_code_label == 'success'


# @responses.activate
# def test_update_default_sms_webhook():
#     build_response(
#         path,
#         'POST',
#         'https://rest.nexmo.com/account/settings',
#         'update_default_sms_webhook.json',
#     )
#     settings_response = account.update_default_sms_webhook(
#         mo_callback_url='https://example.com/inbound_sms_webhook',
#         dr_callback_url='https://example.com/delivery_receipt_webhook',
#     )

#     assert settings_response.mo_callback_url == 'https://example.com/inbound_sms_webhook'
#     assert (
#         settings_response.dr_callback_url
#         == 'https://example.com/delivery_receipt_webhook'
#     )
#     assert settings_response.max_outbound_request == 30
#     assert settings_response.max_inbound_request == 30
#     assert settings_response.max_calls_per_second == 30


# @responses.activate
# def test_list_secrets():
#     build_response(
#         path,
#         'GET',
#         'https://api.nexmo.com/accounts/test_api_key/secrets',
#         'list_secrets.json',
#     )
#     secrets = account.list_secrets()

#     assert len(secrets) == 1
#     assert secrets[0].id == '1b1b1b1b-1b1b-1b-1b1b-1b1b1b1b1b1b'
#     assert secrets[0].created_at == '2022-03-28T14:16:56Z'


# @responses.activate
# def test_create_secret():
#     build_response(
#         path,
#         'POST',
#         'https://api.nexmo.com/accounts/test_api_key/secrets',
#         'secret.json',
#         201,
#     )
#     secret = account.create_secret('Mytestsecret1234')

#     assert account.http_client.last_response.status_code == 201
#     assert secret.id == 'ad6dc56f-07b5-46e1-a527-85530e625800'
#     assert secret.created_at == '2017-03-02T16:34:49Z'


# def test_create_secret_invalid_secret():
#     with raises(InvalidSecretError) as e:
#         account.create_secret('secret')

#     with raises(InvalidSecretError) as e:
#         account.create_secret('MYTESTSECRET1234')

#     with raises(InvalidSecretError) as e:
#         account.create_secret('mytestsecret1234')

#     with raises(InvalidSecretError) as e:
#         account.create_secret('Mytestsecret')

#     assert e.match(
#         'Secret must be 8-25 characters long and contain at least one uppercase letter, one lowercase letter, and one digit.'
#     )


# @responses.activate
# def test_create_secret_error_max_number():
#     build_response(
#         path,
#         'POST',
#         'https://api.nexmo.com/accounts/test_api_key/secrets',
#         'create_secret_error_max_number.json',
#         403,
#     )

#     with raises(ForbiddenError) as e:
#         account.create_secret('Mytestsecret23456')
#     assert 'Account reached maximum number [2] of allowed secrets' in e.exconly()


# @responses.activate
# def test_get_secret():
#     build_response(
#         path,
#         'GET',
#         'https://api.nexmo.com/accounts/test_api_key/secrets/secret_id',
#         'secret.json',
#     )
#     secret = account.get_secret('secret_id')

#     assert secret.id == 'ad6dc56f-07b5-46e1-a527-85530e625800'
#     assert secret.created_at == '2017-03-02T16:34:49Z'


# @responses.activate
# def test_revoke_api_secret():
#     responses.add(
#         responses.DELETE,
#         'https://api.nexmo.com/accounts/test_api_key/secrets/secret_id',
#         status=204,
#     )
#     account.revoke_secret('secret_id')
#     assert account.http_client.last_response.status_code == 204


# @responses.activate
# def test_revoke_api_secret_error_last_secret():
#     build_response(
#         path,
#         'DELETE',
#         'https://api.nexmo.com/accounts/test_api_key/secrets/secret_id',
#         'revoke_secret_error.json',
#         403,
#     )

#     with raises(ForbiddenError) as e:
#         account.revoke_secret('secret_id')

#     assert 'Can not delete the last secret.' in e.exconly()
