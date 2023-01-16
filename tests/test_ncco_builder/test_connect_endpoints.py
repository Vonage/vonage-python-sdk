from vonage import ConnectEndpoints, Ncco
import ncco_samples.ncco_action_samples as nas

import json
import pytest
from pydantic import ValidationError


def _action_as_dict(action: Ncco.Action):
    return action.dict(exclude_none=True)


def test_connect_all_endpoints_from_model():
    phone = ConnectEndpoints.PhoneEndpoint(
        number='447000000000',
        dtmfAnswer='1p2p3p#**903#',
        onAnswer={"url": "https://example.com/answer", "ringbackTone": "http://example.com/ringbackTone.wav"},
    )
    connect_phone = Ncco.Connect(endpoint=phone)
    assert json.dumps(_action_as_dict(connect_phone)) == nas.connect_phone

    app = ConnectEndpoints.AppEndpoint(user='test_user')
    connect_app = Ncco.Connect(endpoint=app)
    assert json.dumps(_action_as_dict(connect_app)) == nas.connect_app

    websocket = ConnectEndpoints.WebsocketEndpoint(
        uri='ws://example.com/socket', contentType='audio/l16;rate=8000', headers={"language": "en-GB"}
    )
    connect_websocket = Ncco.Connect(endpoint=websocket)
    assert json.dumps(_action_as_dict(connect_websocket)) == nas.connect_websocket

    sip = ConnectEndpoints.SipEndpoint(
        uri='sip:rebekka@sip.mcrussell.com', headers={"location": "New York City", "occupation": "developer"}
    )
    connect_sip = Ncco.Connect(endpoint=sip)
    assert json.dumps(_action_as_dict(connect_sip)) == nas.connect_sip

    vbc = ConnectEndpoints.VbcEndpoint(extension='111')
    connect_vbc = Ncco.Connect(endpoint=vbc)
    assert json.dumps(_action_as_dict(connect_vbc)) == nas.connect_vbc


def test_connect_endpoints_errors():
    with pytest.raises(ValidationError) as err:
        ConnectEndpoints.PhoneEndpoint(number='447000000000', onAnswer={'url': 'not-a-valid-url'})

    with pytest.raises(ValidationError) as err:
        ConnectEndpoints.PhoneEndpoint(
            number='447000000000',
            onAnswer={'url': 'http://example.com/answer', 'ringbackTone': 'not-a-valid-url'},
        )

    with pytest.raises(ValueError) as err:
        ConnectEndpoints.create_endpoint_model_from_dict({'type': 'carrier_pigeon'})
    assert (
        str(err.value)
        == 'Invalid "type" specified for endpoint object. Cannot create a ConnectEndpoints.Endpoint model.'
    )
