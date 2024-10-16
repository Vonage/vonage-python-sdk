from os.path import abspath
from unittest.mock import MagicMock, patch

import responses
from vonage_http_client.http_client import HttpClient
from vonage_network_sim_swap import NetworkSimSwap

from testutils import build_response, get_mock_jwt_auth

path = abspath(__file__)

sim_swap = NetworkSimSwap(HttpClient(get_mock_jwt_auth()))


def test_http_client_property():
    http_client = sim_swap.http_client
    assert isinstance(http_client, HttpClient)


@patch('vonage_network_auth.NetworkAuth.get_sim_swap_camara_token')
@responses.activate
def test_check_sim_swap(mock_get_oauth2_user_token: MagicMock):
    build_response(
        path,
        'POST',
        'https://api-eu.vonage.com/camara/sim-swap/v040/check',
        'check_sim_swap.json',
    )
    mock_get_oauth2_user_token.return_value = 'token'

    response = sim_swap.check('447700900000', max_age=24)

    assert response['swapped'] == True


@patch('vonage_network_auth.NetworkAuth.get_sim_swap_camara_token')
@responses.activate
def test_get_last_swap_date(mock_get_oauth2_user_token: MagicMock):
    build_response(
        path,
        'POST',
        'https://api-eu.vonage.com/camara/sim-swap/v040/retrieve-date',
        'get_swap_date.json',
    )
    mock_get_oauth2_user_token.return_value = 'token'

    response = sim_swap.get_last_swap_date('447700900000')

    assert response['latestSimChange'] == '2023-12-22T04:00:44.000Z'
