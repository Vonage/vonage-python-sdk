from dataclasses import asdict
from os.path import abspath

import responses
from http_client.auth import Auth
from pydantic import ValidationError
from pytest import raises
from testing_utils import build_response
from utils import remove_none_values

from http_client.http_client import HttpClient
from number_insight_v2.number_insight_v2 import (
    FraudCheckRequest,
    FraudCheckResponse,
    NumberInsightV2,
)

path = abspath(__file__)

ni2 = NumberInsightV2(HttpClient(Auth('key', 'secret')))


def test_fraud_check_request_defaults():
    request = FraudCheckRequest(phone='1234567890')
    assert request.type == 'phone'
    assert request.phone == '1234567890'
    assert request.insights == ['fraud_score', 'sim_swap']


def test_fraud_check_request_custom_insights():
    request = FraudCheckRequest(phone='1234567890', insights=['fraud_score'])
    assert request.type == 'phone'
    assert request.phone == '1234567890'
    assert request.insights == ['fraud_score']


def test_fraud_check_request_invalid_insights():
    with raises(ValidationError):
        FraudCheckRequest(phone='1234567890', insights=['invalid_insight'])


@responses.activate
def test_ni2_defaults():
    build_response(path, 'POST', 'https://api.nexmo.com/v2/ni', 'default.json')
    request = FraudCheckRequest(phone='1234567890')
    response = ni2.fraud_check(request)
    assert type(response) == FraudCheckResponse
    assert response.request_id == '2c2f5d3f-93ac-42b1-9083-4b14f0d583d3'
    assert response.phone.carrier == 'Verizon Wireless'
    assert response.fraud_score.risk_score == '0'
    assert response.sim_swap.status == 'completed'


@responses.activate
def test_ni2_fraud_score_only():
    build_response(path, 'POST', 'https://api.nexmo.com/v2/ni', 'fraud_score.json')
    request = FraudCheckRequest(phone='1234567890', insights=['fraud_score'])
    response = ni2.fraud_check(request)
    assert type(response) == FraudCheckResponse
    assert response.request_id == '2c2f5d3f-93ac-42b1-9083-4b14f0d583d3'
    assert response.phone.carrier == 'Verizon Wireless'
    assert response.fraud_score.risk_score == '0'
    assert response.sim_swap is None

    clear_response = asdict(response, dict_factory=remove_none_values)
    print(clear_response)
    assert 'fraud_score' in clear_response
    assert 'sim_swap' not in clear_response


@responses.activate
def test_ni2_sim_swap_only():
    build_response(path, 'POST', 'https://api.nexmo.com/v2/ni', 'sim_swap.json')
    request = FraudCheckRequest(phone='1234567890', insights='sim_swap')
    response = ni2.fraud_check(request)
    assert type(response) == FraudCheckResponse
    assert response.request_id == 'db5282b6-8046-4217-9c0e-d9c55d8696e9'
    assert response.phone.phone == '1234567890'
    assert response.fraud_score is None
    assert response.sim_swap.status == 'completed'
    assert response.sim_swap.swapped is False

    clear_response = asdict(response, dict_factory=remove_none_values)
    assert 'fraud_score' not in clear_response
    assert 'sim_swap' in clear_response
    assert 'reason' not in clear_response['sim_swap']
