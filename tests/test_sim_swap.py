from vonage.sim_swap import SimSwap
from util import *

import responses


@responses.activate
def test_check_sim_swap(sim_swap: SimSwap):
    stub(
        responses.POST,
        'https://api-eu.vonage.com/oauth2/bc-authorize',
        fixture_path='camara_auth/oidc_request.json',
    )
    stub(
        responses.POST,
        'https://api-eu.vonage.com/oauth2/token',
        fixture_path='camara_auth/token_request.json',
    )
    stub(
        responses.POST,
        'https://api-eu.vonage.com/camara/sim-swap/v040/check',
        fixture_path='sim_swap/check_sim_swap.json',
    )

    response = sim_swap.check('447700900000', max_age=24)

    assert response['swapped'] == True


@responses.activate
def test_get_last_swap_date(sim_swap: SimSwap):
    stub(
        responses.POST,
        'https://api-eu.vonage.com/oauth2/bc-authorize',
        fixture_path='camara_auth/oidc_request.json',
    )
    stub(
        responses.POST,
        'https://api-eu.vonage.com/oauth2/token',
        fixture_path='camara_auth/token_request.json',
    )
    stub(
        responses.POST,
        'https://api-eu.vonage.com/camara/sim-swap/v040/retrieve-date',
        fixture_path='sim_swap/get_swap_date.json',
    )

    response = sim_swap.get_last_swap_date('447700900000')

    assert response['latestSimChange'] == '2019-08-24T14:15:22Z'
