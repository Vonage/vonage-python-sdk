from os.path import abspath

import responses
from pytest import raises

from vonage_numbers.errors import NumbersError
from vonage_numbers.number_management import Numbers
from vonage_http_client.http_client import HttpClient

from testutils import build_response, get_mock_api_key_auth
from vonage_numbers.requests import (
    ListOwnedNumbersFilter,
    NumberParams,
    SearchAvailableNumbersFilter,
    UpdateNumberParams,
)

path = abspath(__file__)

numbers = Numbers(HttpClient(get_mock_api_key_auth()))


def test_http_client_property():
    http_client = numbers.http_client
    assert isinstance(http_client, HttpClient)


def test_filter_properties():
    with raises(NumbersError) as err:
        ListOwnedNumbersFilter(pattern='123')
    assert err.match(
        '"search_pattern" is required when "pattern"" is provided and vice versa.'
    )


@responses.activate
def test_list_owned_numbers_basic():
    build_response(
        path,
        'GET',
        'https://rest.nexmo.com/account/numbers',
        'list_owned_numbers_basic.json',
    )
    numbers_list, count, next_page = numbers.list_owned_numbers()

    assert len(numbers_list) == 2
    assert numbers_list[0].msisdn == '3400000000'
    assert numbers_list[0].country == 'ES'
    assert numbers_list[1].msisdn == '447007000000'
    assert numbers_list[1].country == 'GB'
    assert numbers_list[1].features == ['VOICE', 'SMS']
    assert numbers_list[1].type == 'mobile-lvn'
    assert count == 2
    assert next_page is None


@responses.activate
def test_list_owned_numbers_with_filter():
    build_response(
        path,
        'GET',
        'https://rest.nexmo.com/account/numbers',
        'list_owned_numbers_filter.json',
    )
    numbers_list, count, next_page = numbers.list_owned_numbers(
        ListOwnedNumbersFilter(application_id='29f769u7-7ce1-46c9-ade3-f2dedee4fr4t')
    )

    assert len(numbers_list) == 1
    assert numbers_list[0].msisdn == '447007000000'
    assert numbers_list[0].voice_callback_type == 'app'
    assert numbers_list[0].voice_callback_value == '29f769u7-7ce1-46c9-ade3-f2dedee4fr4t'
    assert numbers_list[0].app_id == '29f769u7-7ce1-46c9-ade3-f2dedee4fr4t'
    assert count == 1
    assert next_page is None


@responses.activate
def test_list_owned_numbers_subset():
    build_response(
        path,
        'GET',
        'https://rest.nexmo.com/account/numbers',
        'list_owned_numbers_subset.json',
    )
    numbers_list, count, next_page = numbers.list_owned_numbers(
        ListOwnedNumbersFilter(size=1)
    )

    assert len(numbers_list) == 1
    assert numbers_list[0].msisdn == '3400000000'
    assert count == 2
    assert next_page == 2


@responses.activate
def test_search_available_numbers_basic():
    build_response(
        path,
        'GET',
        'https://rest.nexmo.com/number/search',
        'search_available_numbers_basic.json',
    )
    numbers_list, count, next_page = numbers.search_available_numbers(
        SearchAvailableNumbersFilter(country='GB', size=3)
    )

    assert len(numbers_list) == 3
    assert numbers_list[0].msisdn == '442039050911'
    assert count == 8353
    assert next_page is 2


@responses.activate
def test_search_available_numbers_with_filter():
    build_response(
        path,
        'GET',
        'https://rest.nexmo.com/number/search',
        'search_available_numbers_filter.json',
    )
    numbers_list, count, next_page = numbers.search_available_numbers(
        SearchAvailableNumbersFilter(
            country='GB',
            size=1,
            index=1,
            pattern='44203905',
            search_pattern=1,
            type='landline',
            features='VOICE',
        )
    )

    assert len(numbers_list) == 1
    assert numbers_list[0].msisdn == '442039055555'
    assert numbers_list[0].country == 'GB'
    assert numbers_list[0].features == ['VOICE']
    assert numbers_list[0].type == 'landline'
    assert count == 2
    assert next_page == 2


@responses.activate
def test_search_available_numbers_end_of_list():
    build_response(
        path,
        'GET',
        'https://rest.nexmo.com/number/search',
        'search_available_numbers_end_of_list.json',
    )
    numbers_list, count, next_page = numbers.search_available_numbers(
        SearchAvailableNumbersFilter(
            country='GB', size=3, pattern='44203905', search_pattern=0
        )
    )

    assert len(numbers_list) == 1
    assert numbers_list[0].msisdn == '442039055555'
    assert count == 1
    assert next_page is None


@responses.activate
def test_empty_response():
    build_response(
        path,
        'GET',
        'https://rest.nexmo.com/account/numbers',
        'nothing.json',
    )
    numbers_list, count, next_page = numbers.list_owned_numbers(
        ListOwnedNumbersFilter(pattern='12345612345', search_pattern=1)
    )

    assert len(numbers_list) == 0
    assert count == 0
    assert next_page is None

    build_response(
        path,
        'GET',
        'https://rest.nexmo.com/number/search',
        'nothing.json',
    )
    numbers_list, count, next_page = numbers.search_available_numbers(
        SearchAvailableNumbersFilter(
            country='GB', size=3, pattern='12345612345', search_pattern=1
        )
    )

    assert len(numbers_list) == 0
    assert count == 0
    assert next_page is None


@responses.activate
def test_buy_number():
    build_response(
        path,
        'POST',
        'https://rest.nexmo.com/number/buy',
        'number.json',
    )
    response = numbers.buy_number(NumberParams(country='GB', msisdn='447000000000'))

    assert response.error_code == '200'
    assert response.error_code_label == 'success'


@responses.activate
def test_cancel_number():
    build_response(
        path,
        'POST',
        'https://rest.nexmo.com/number/cancel',
        'number.json',
    )
    response = numbers.cancel_number(NumberParams(country='GB', msisdn='447000000000'))

    assert response.error_code == '200'
    assert response.error_code_label == 'success'


@responses.activate
def test_cancel_number_error_no_number():
    build_response(
        path,
        'POST',
        'https://rest.nexmo.com/number/cancel',
        'no_number.json',
    )
    with raises(NumbersError) as e:
        numbers.cancel_number(NumberParams(country='GB', msisdn='447000000000'))

    assert e.match('method failed')


@responses.activate
def test_update_number():
    build_response(
        path,
        'POST',
        'https://rest.nexmo.com/number/update',
        'number.json',
    )
    response = numbers.update_number(
        UpdateNumberParams(
            country='GB',
            msisdn='447009000000',
            app_id='29f769u7-7ce1-46c9-ade3-f2dedee4fr4t',
            mo_http_url='https://example.com',
            mo_smpp_sytem_type='inbound',
            voice_callback_type='tel',
            voice_callback_value='447009000000',
            voice_status_callback='https://example.com',
        )
    )

    assert response.error_code == '200'
    assert response.error_code_label == 'success'


def test_update_number_options_error():
    with raises(NumbersError) as e:
        UpdateNumberParams(
            country='GB',
            msisdn='447009000000',
            voice_callback_value='447009000000',
        )

    assert e.match(
        '"voice_callback_value" is required when "voice_callback_type" is provided, and vice versa.'
    )
