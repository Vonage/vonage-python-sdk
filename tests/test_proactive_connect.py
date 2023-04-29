from vonage.errors import ProactiveConnectError, ClientError
from util import *

import responses
from pytest import raises


@responses.activate
def test_list_all_lists(proc, dummy_data):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/v0.1/bulk/lists',
        fixture_path='proactive_connect/list_lists.json',
    )

    lists = proc.list_all_lists()
    assert request_user_agent() == dummy_data.user_agent
    assert lists['total_items'] == 2
    assert lists['_embedded']['lists'][0]['name'] == 'Recipients for demo'
    assert lists['_embedded']['lists'][0]['id'] == 'af8a84b6-c712-4252-ac8d-6e28ac9317ce'
    assert lists['_embedded']['lists'][1]['name'] == 'Salesforce contacts'
    assert lists['_embedded']['lists'][1]['datasource']['type'] == 'salesforce'


@responses.activate
def test_list_all_lists_options(proc):
    stub(
        responses.GET,
        'https://api-eu.vonage.com/v0.1/bulk/lists',
        fixture_path='proactive_connect/list_lists.json',
    )

    lists = proc.list_all_lists(page=1, page_size=5)
    assert lists['total_items'] == 2
    assert lists['_embedded']['lists'][0]['name'] == 'Recipients for demo'
    assert lists['_embedded']['lists'][0]['id'] == 'af8a84b6-c712-4252-ac8d-6e28ac9317ce'
    assert lists['_embedded']['lists'][1]['name'] == 'Salesforce contacts'


def test_list_all_lists_invalid_options_error(proc):
    with raises(ProactiveConnectError) as err:
        proc.list_all_lists(page=-1)
    assert str(err.value) == '"page" must be an int > 0.'

    with raises(ProactiveConnectError) as err:
        proc.list_all_lists(page_size=-1)
    assert str(err.value) == '"page_size" must be an int > 0.'


@responses.activate
def test_create_list_basic(proc):
    stub(
        responses.POST,
        'https://api-eu.vonage.com/v0.1/bulk/lists',
        fixture_path='proactive_connect/create_list_basic.json',
        status_code=201,
    )

    list = proc.create_list({'name': 'my_list'})
    assert list['id'] == '6994fd17-7691-4463-be16-172ab1430d97'
    assert list['name'] == 'my_list'


@responses.activate
def test_create_list_manual(proc):
    stub(
        responses.POST,
        'https://api-eu.vonage.com/v0.1/bulk/lists',
        fixture_path='proactive_connect/create_list_manual.json',
        status_code=201,
    )

    params = {
        "name": "my name",
        "description": "my description",
        "tags": ["vip", "sport"],
        "attributes": [{"name": "phone_number", "alias": "phone"}],
        "datasource": {"type": "manual"},
    }

    list = proc.create_list(params)
    assert list['id'] == '9508e7b8-fe99-4fdf-b022-65d7e461db2d'
    assert list['name'] == 'my_list'
    assert list['description'] == 'my description'
    assert list['tags'] == ['vip', 'sport']
    assert list['attributes'][0]['name'] == 'phone_number'


@responses.activate
def test_create_list_salesforce(proc):
    stub(
        responses.POST,
        'https://api-eu.vonage.com/v0.1/bulk/lists',
        fixture_path='proactive_connect/create_list_salesforce.json',
        status_code=201,
    )

    params = {
        "name": "my name",
        "description": "my description",
        "tags": ["vip", "sport"],
        "attributes": [{"name": "phone_number", "alias": "phone"}],
        "datasource": {
            "type": "salesforce",
            "integration_id": "salesforce_credentials",
            "soql": "select Id, LastName, FirstName, Phone, Email FROM Contact",
        },
    }

    list = proc.create_list(params)
    assert list['id'] == '246d17c4-79e6-4a25-8b4e-b777a83f6c30'
    assert list['name'] == 'my_salesforce_list'
    assert list['description'] == 'my salesforce description'
    assert list['datasource']['type'] == 'salesforce'
    assert list['datasource']['integration_id'] == 'salesforce_credentials'
    assert list['datasource']['soql'] == 'select Id, LastName, FirstName, Phone, Email FROM Contact'


def test_create_list_errors(proc):
    params = {
        "name": "my name",
        "datasource": {
            "type": "salesforce",
            "integration_id": 1234,
            "soql": "select Id, LastName, FirstName, Phone, Email FROM Contact",
        },
    }

    with raises(ProactiveConnectError) as err:
        proc.create_list({})
    assert str(err.value) == 'You must supply a name for the new list.'

    with raises(ProactiveConnectError) as err:
        proc.create_list(params)
    assert str(err.value) == 'You must supply values for "integration_id" and "soql" as strings.'

    with raises(ProactiveConnectError) as err:
        params['datasource'].pop('integration_id')
        proc.create_list(params)
    assert (
        str(err.value)
        == 'You must supply a value for "integration_id" and "soql" when creating a list with Salesforce.'
    )


@responses.activate
def test_create_list_invalid_name_error(proc):
    stub(
        responses.POST,
        'https://api-eu.vonage.com/v0.1/bulk/lists',
        fixture_path='proactive_connect/create_list_400.json',
        status_code=400,
    )

    with raises(ClientError) as err:
        proc.create_list({'name': 1234})
    assert (
        str(err.value)
        == 'Request data did not validate: Bad Request (https://developer.vonage.com/en/api-errors)\nError: name must be longer than or equal to 1 and shorter than or equal to 255 characters\nError: name must be a string'
    )


@responses.activate
def test_get_list(proc):
    list_id = '9508e7b8-fe99-4fdf-b022-65d7e461db2d'
    stub(
        responses.GET,
        f'https://api-eu.vonage.com/v0.1/bulk/lists/{list_id}',
        fixture_path='proactive_connect/get_list.json',
    )

    list = proc.get_list(list_id)
    assert list['id'] == '9508e7b8-fe99-4fdf-b022-65d7e461db2d'
    assert list['name'] == 'my_list'
    assert list['tags'] == ['vip', 'sport']


@responses.activate
def test_get_list_404(proc):
    list_id = 'a508e7b8-fe99-4fdf-b022-65d7e461db2d'
    stub(
        responses.GET,
        f'https://api-eu.vonage.com/v0.1/bulk/lists/{list_id}',
        fixture_path='proactive_connect/get_list_404.json',
        status_code=404,
    )

    with raises(ClientError) as err:
        proc.get_list(list_id)
    assert (
        str(err.value)
        == 'The requested resource does not exist: Not Found (https://developer.vonage.com/en/api-errors)'
    )


@responses.activate
def test_update_list(proc):
    list_id = '9508e7b8-fe99-4fdf-b022-65d7e461db2d'
    stub(
        responses.PUT,
        f'https://api-eu.vonage.com/v0.1/bulk/lists/{list_id}',
        fixture_path='proactive_connect/update_list.json',
    )

    params = {'name': 'my_list', 'tags': ['vip', 'sport', 'football']}
    list = proc.update_list(list_id, params)
    assert list['id'] == '9508e7b8-fe99-4fdf-b022-65d7e461db2d'
    assert list['tags'] == ['vip', 'sport', 'football']
    assert list['description'] == 'my updated description'
    assert list['updated_at'] == '2023-04-28T21:39:17.825Z'


@responses.activate
def test_update_list_salesforce(proc):
    list_id = '246d17c4-79e6-4a25-8b4e-b777a83f6c30'
    stub(
        responses.PUT,
        f'https://api-eu.vonage.com/v0.1/bulk/lists/{list_id}',
        fixture_path='proactive_connect/update_list_salesforce.json',
    )

    params = {'name': 'my_list', 'tags': ['music']}
    list = proc.update_list(list_id, params)
    assert list['id'] == list_id
    assert list['tags'] == ['music']
    assert list['updated_at'] == '2023-04-28T22:23:37.054Z'


def test_update_list_name_error(proc):
    with raises(ProactiveConnectError) as err:
        proc.update_list('9508e7b8-fe99-4fdf-b022-65d7e461db2d', {'description': 'my new description'})
    assert str(err.value) == 'You must supply a name for the new list.'


@responses.activate
def test_delete_list(proc):
    list_id = '9508e7b8-fe99-4fdf-b022-65d7e461db2d'
    stub(
        responses.DELETE,
        f'https://api-eu.vonage.com/v0.1/bulk/lists/{list_id}',
        fixture_path='null.json',
        status_code=204,
    )

    assert proc.delete_list(list_id) == None


@responses.activate
def test_delete_list_404(proc):
    list_id = '9508e7b8-fe99-4fdf-b022-65d7e461db2d'
    stub(
        responses.DELETE,
        f'https://api-eu.vonage.com/v0.1/bulk/lists/{list_id}',
        fixture_path='proactive_connect/list_404.json',
        status_code=404,
    )
    with raises(ClientError) as err:
        proc.delete_list(list_id)
    assert (
        str(err.value)
        == 'The requested resource does not exist: Not Found (https://developer.vonage.com/en/api-errors)'
    )


@responses.activate
def test_clear_list(proc):
    list_id = '9508e7b8-fe99-4fdf-b022-65d7e461db2d'
    stub(
        responses.POST,
        f'https://api-eu.vonage.com/v0.1/bulk/lists/{list_id}/clear',
        fixture_path='null.json',
        status_code=202,
    )

    assert proc.clear_list(list_id) == None


@responses.activate
def test_clear_list_404(proc):
    list_id = '9508e7b8-fe99-4fdf-b022-65d7e461db2d'
    stub(
        responses.POST,
        f'https://api-eu.vonage.com/v0.1/bulk/lists/{list_id}/clear',
        fixture_path='proactive_connect/list_404.json',
        status_code=404,
    )
    with raises(ClientError) as err:
        proc.clear_list(list_id)
    assert (
        str(err.value)
        == 'The requested resource does not exist: Not Found (https://developer.vonage.com/en/api-errors)'
    )


@responses.activate
def test_sync_list_from_datasource(proc):
    list_id = '246d17c4-79e6-4a25-8b4e-b777a83f6c30'
    stub(
        responses.POST,
        f'https://api-eu.vonage.com/v0.1/bulk/lists/{list_id}/fetch',
        fixture_path='null.json',
        status_code=202,
    )

    assert proc.sync_list_from_datasource(list_id) == None


@responses.activate
def test_sync_list_manual_datasource_error(proc):
    list_id = '9508e7b8-fe99-4fdf-b022-65d7e461db2d'
    stub(
        responses.POST,
        f'https://api-eu.vonage.com/v0.1/bulk/lists/{list_id}/fetch',
        fixture_path='proactive_connect/fetch_list_400.json',
        status_code=400,
    )

    with raises(ClientError) as err:
        proc.sync_list_from_datasource(list_id) == None
    assert (
        str(err.value)
        == 'Request data did not validate: Cannot Fetch a manual list (https://developer.vonage.com/en/api-errors)'
    )


@responses.activate
def test_sync_list_from_datasource_404(proc):
    list_id = '346d17c4-79e6-4a25-8b4e-b777a83f6c30'
    stub(
        responses.POST,
        f'https://api-eu.vonage.com/v0.1/bulk/lists/{list_id}/clear',
        fixture_path='proactive_connect/list_404.json',
        status_code=404,
    )
    with raises(ClientError) as err:
        proc.clear_list(list_id)
    assert (
        str(err.value)
        == 'The requested resource does not exist: Not Found (https://developer.vonage.com/en/api-errors)'
    )
