from vonage import Client, ClientError, ServerError, NumberInsightV2Error
from util import stub

from pytest import raises
import responses


api_key = '1234asdf'
api_secret = 'qwerasdfzxcv'
client = Client(key=api_key, secret=api_secret)
ni2 = client.number_insight_v2
ni2_url = f'https://{client.api_host()}/v2/ni'
insight_number = '12345678901'


@responses.activate
def test_fraud_score_string():
    stub(responses.POST, ni2_url, fixture_path='number_insight_v2/fraud_score.json')
    response = ni2.fraud_check(insight_number, 'fraud_score')

    assert response['type'] == 'phone'
    assert response['phone']['carrier'] == 'Verizon Wireless'
    assert response['phone']['type'] == 'MOBILE'
    assert response['fraud_score']['risk_score'] == '50'
    assert response['fraud_score']['risk_recommendation'] == 'flag'


@responses.activate
def test_fraud_score_list():
    stub(responses.POST, ni2_url, fixture_path='number_insight_v2/fraud_score.json')
    response = ni2.fraud_check(insight_number, ['fraud_score'])

    assert response['type'] == 'phone'
    assert response['phone']['carrier'] == 'Verizon Wireless'
    assert response['phone']['type'] == 'MOBILE'
    assert response['fraud_score']['risk_score'] == '50'
    assert response['fraud_score']['risk_recommendation'] == 'flag'


@responses.activate
def test_sim_swap_string_success():
    stub(responses.POST, ni2_url, fixture_path='number_insight_v2/sim_swap_success.json')
    response = ni2.fraud_check(insight_number, 'sim_swap')

    assert response['type'] == 'phone'
    assert response['phone']['phone'] == insight_number
    assert response['sim_swap']['status'] == 'completed'
    assert response['sim_swap']['swapped'] == False


@responses.activate
def test_sim_swap_list_failure():
    stub(responses.POST, ni2_url, fixture_path='number_insight_v2/sim_swap_failure.json')
    response = ni2.fraud_check(insight_number, ['sim_swap'])

    assert response['type'] == 'phone'
    assert response['phone']['phone'] == insight_number
    assert response['sim_swap']['status'] == 'failed'
    assert response['sim_swap']['reason'] == 'Mobile Network Operator Not Supported'


@responses.activate
def test_fraud_score_and_sim_swap():
    stub(responses.POST, ni2_url, fixture_path='number_insight_v2/fraud_score_and_sim_swap.json')
    response = ni2.fraud_check(insight_number, ['fraud_score', 'sim_swap'])

    assert response['type'] == 'phone'
    assert response['phone']['phone'] == insight_number
    assert response['phone']['carrier'] == 'Verizon Wireless'
    assert response['phone']['type'] == 'MOBILE'
    assert response['fraud_score']['risk_score'] == '0'
    assert response['fraud_score']['risk_recommendation'] == 'allow'
    assert response['fraud_score']['label'] == 'low'
    assert response['fraud_score']['status'] == 'completed'
    assert response['sim_swap']['status'] == 'completed'
    assert response['sim_swap']['swapped'] == False


def test_error_insights_has_invalid_type():
    with raises(NumberInsightV2Error) as err:
        ni2.fraud_check(insight_number, 1234)
    assert (
        str(err.value)
        == f'You must pass in values for the "insights" parameter as a string or a list.'
    )


def test_invalid_insight_error():
    with raises(NumberInsightV2Error) as err:
        ni2.fraud_check(insight_number, 'an_invalid_insight')
    assert (
        str(err.value)
        == f'The only insights that can be requested are "fraud_score" and "sim_swap". You requested: "an_invalid_insight".'
    )


@responses.activate
def test_error_unauthorized():
    stub(
        responses.POST,
        ni2_url,
        fixture_path='number_insight_v2/unauthorized.json',
        status_code=401,
    )
    bad_client = Client(key='12345678', secret='an-invalid-secret')

    with raises(ClientError) as err:
        bad_client.number_insight_v2.fraud_check(insight_number, 'fraud_score')
    assert str(err.value) == 'Authentication failed.'


@responses.activate
def test_error_rate_limited():
    stub(
        responses.POST,
        ni2_url,
        fixture_path='number_insight_v2/rate_limited.json',
        status_code=429,
    )

    with raises(ClientError) as err:
        ni2.fraud_check(insight_number, 'fraud_score')
    assert (
        str(err.value)
        == 'Rate Limit Hit: Please wait, then retry your request (https://developer.vonage.com/api-errors#rate-limit)'
    )


@responses.activate
def test_error_third_party_server():
    stub(
        responses.POST,
        ni2_url,
        fixture_path='number_insight_v2/server_error.json',
        status_code=500,
    )
    unprocessable_number = '111111111111'

    with raises(ServerError) as err:
        ni2.fraud_check(unprocessable_number, 'fraud_score')
    assert str(err.value) == '500 response from api.nexmo.com'
