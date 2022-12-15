import vonage
from util import *
from vonage.errors import SmsError, PartialFailureError


@responses.activate
def test_send_message(sms, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/sms/json",
        fixture_path='sms/send_message.json')

    params = {"from": "Python", "to": "447525856424", "text": "Hey!"}

    assert isinstance(sms.send_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "from=Python" in request_body()
    assert "to=447525856424" in request_body()
    assert "text=Hey%21" in request_body()


@responses.activate
def test_send_message_200_error(sms, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/sms/json",
        fixture_path='sms/send_message_200_error.json')

    params = {"from": "Python", "text": "Hey!"}

    with pytest.raises(SmsError) as err:
        assert isinstance(sms.send_message(params), dict)
        assert str(err.value) == 'Sms.send_message method failed with error code 2: Missing to param'

    assert request_user_agent() == dummy_data.user_agent
    assert "from=Python" in request_body()
    assert "text=Hey%21" in request_body()


@responses.activate
def test_send_long_message(sms, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/sms/json",
        fixture_path='sms/send_long_message.json')

    with open('tests/data/sms/long_message.txt', 'r') as reader:
        long_message = reader.read()

    params = {"from": "Python", "to": "447525856424", "text": long_message}
    response_data = sms.send_message(params)

    assert isinstance(response_data, dict)
    assert response_data['message-count'] == '2'
    assert request_user_agent() == dummy_data.user_agent
    assert "from=Python" in request_body()
    assert "to=447525856424" in request_body()
    assert f"text={long_message.replace(' ', '+').replace(',', '%2C')}" in request_body() # Check for encoding


@responses.activate
def test_send_long_message_partial_error(sms, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/sms/json",
        fixture_path='sms/send_long_message_partial_error.json')

    with open('tests/data/sms/long_message.txt', 'r') as reader:
        long_message = reader.read()

    params = {"from": "Python", "to": "447525856424", "text": long_message}
    
    with pytest.raises(PartialFailureError) as err:
        assert isinstance(sms.send_message(params), dict)
        assert str(err.value) == 'Sms.send_message method partially failed. Not all of the message sent successfully.'


@responses.activate
def test_authentication_error(sms):
    responses.add(responses.POST, "https://rest.nexmo.com/sms/json", status=401)

    with pytest.raises(vonage.AuthenticationError):
        sms.send_message({})


@responses.activate
def test_client_error(sms):
    responses.add(responses.POST, "https://rest.nexmo.com/sms/json", status=400)

    with pytest.raises(vonage.ClientError) as excinfo:
        sms.send_message({})
    excinfo.match(r"400 response from rest.nexmo.com")


@responses.activate
def test_server_error(sms):
    responses.add(responses.POST, "https://rest.nexmo.com/sms/json", status=500)

    with pytest.raises(vonage.ServerError) as excinfo:
        sms.send_message({})
    excinfo.match(r"500 response from rest.nexmo.com")


@responses.activate
def test_submit_sms_conversion(sms):
    responses.add(
        responses.POST, "https://api.nexmo.com/conversions/sms", status=200, body=b"OK"
    )

    sms.submit_sms_conversion("a-message-id")
    assert "message-id=a-message-id" in request_body()
    assert "timestamp" in request_body()
