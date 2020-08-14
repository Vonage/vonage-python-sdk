import nexmo, json
from util import *


@responses.activate
def test_send_message(sms, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/sms/json")

    params = {"from": "Python", "to": "447525856424", "text": "Hey!"}

    assert isinstance(sms.send_message(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "from=Python" in request_body()
    assert "to=447525856424" in request_body()
    assert "text=Hey%21" in request_body()


@responses.activate
def test_authentication_error(sms):
    responses.add(responses.POST, "https://rest.nexmo.com/sms/json", status=401)

    with pytest.raises(nexmo.AuthenticationError):
        sms.send_message({})


@responses.activate
def test_client_error(sms):
    responses.add(responses.POST, "https://rest.nexmo.com/sms/json", status=400)

    with pytest.raises(nexmo.ClientError) as excinfo:
        sms.send_message({})
    excinfo.match(r"400 response from rest.nexmo.com")


@responses.activate
def test_missing_param_error(sms):
    responses.add(
        responses.POST,
        "https://rest.nexmo.com/sms/json",
        status=200,
        body=json.dumps(
            {
                "messages": [
                    {
                        "status": "2",
                        "error-text": "Missing from param"
                    }
                ]
            }
        ),
        content_type='application/json'
    )

    with pytest.raises(nexmo.errors.MissingParamError) as excinfo:
        sms.send_message({})
    excinfo.match(r"Missing from param")


@responses.activate
def test_invalid_param_error(sms):
    responses.add(
        responses.POST,
        "https://rest.nexmo.com/sms/json",
        status=200,
        body=json.dumps(
            {
                "messages": [
                    {
                        "status": "3",
                        "error-text": "to address is not numeric"
                    }
                ]
            }
        ),
        content_type='application/json'
    )

    with pytest.raises(nexmo.InvalidParamError) as excinfo:
        sms.send_message({'from': 'Vonage SMS API','to': '8888888888aaa','text': 'Hello from Vonage'})
    excinfo.match(r"to address is not numeric")


@responses.activate
def test_credential_error(sms):
    responses.add(
        responses.POST,
        "https://rest.nexmo.com/sms/json",
        status=200,
        body=json.dumps(
            {
                "messages": [
                    {
                        "status": "4",
                        "error-text": "Bad Credentials"
                    }
                ]
            }
        ),
        content_type='application/json'
    )

    with pytest.raises(nexmo.CredentialError) as excinfo:
        sms.send_message({'from': 'Vonage SMS API','to': '8888888888aaa','text': 'Hello from Vonage'})
    excinfo.match(r"Bad Credentials")


@responses.activate
def test_invalid_message_error(sms):
    responses.add(
        responses.POST,
        "https://rest.nexmo.com/sms/json",
        status=200,
        body=json.dumps(
            {
                "messages": [
                    {
                        "status": "6",
                        "error-text": "Unroutable message - rejected"
                    }
                ]
            }
        ),
        content_type='application/json'
    )

    with pytest.raises(nexmo.InvalidMessageError) as excinfo:
        sms.send_message({'from': 'Vonage SMS API','to': '88888888888','text': 'Hello from Vonage'})
    excinfo.match(r"Unroutable message - rejected")


@responses.activate
def test_invalid_ttl_error(sms):
    responses.add(
        responses.POST,
        "https://rest.nexmo.com/sms/json",
        status=200,
        body=json.dumps(
            {
                "messages": [
                    {
                        "status": "16",
                        "error-text": "value for ttl field out of range"
                    }
                ]
            }
        ),
        content_type='application/json'
    )

    with pytest.raises(nexmo.InvalidTTLError) as excinfo:
        sms.send_message({'ttl':1, 'from': 'Vonage SMS API','to': '88888888888','text': 'Hello from Vonage'})
    excinfo.match(r"value for ttl field out of range")


""" When the signature method in the client definition is not the same defined in the account settings.
sms = Sms(key='API_KEY', signature_secret='LARGE_KEY', signature_method='sha512')
In the user settings md5 hash signature has been defined
"""
@responses.activate
def test_invalid_signature_error(sms):
    responses.add(
        responses.POST,
        "https://rest.nexmo.com/sms/json",
        status=200,
        body=json.dumps(
            {
                "messages": [
                    {
                        "status": "14",
                        "error-text": "Invalid Signature"
                    }
                ]
            }
        ),
        content_type='application/json'
    )

    with pytest.raises(nexmo.InvalidSignatureError) as excinfo:
        sms.send_message({'from': 'Vonage SMS API','to': '88888888888','text': 'Hello from Vonage'})
    excinfo.match(r"Invalid Signature")


@responses.activate
def test_server_error(sms):
    responses.add(responses.POST, "https://rest.nexmo.com/sms/json", status=500)

    with pytest.raises(nexmo.ServerError) as excinfo:
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


@responses.activate
def test_resource_not_found_error(client, sms):
    #changed rest.nexmo.com for api.nexmo.com on purpose
    responses.add(
        responses.POST,
        "https://api.nexmo.com/sms/json",
        status = 404,
        body = b'<html>\r\n<head><title>404 Not Found</title></head>\r\n<body>\r\n<center><h1>404 Not Found</h1></center>\r\n<hr><center>nginx</center>\r\n</body>\r\n</html>\r\n'
    )

    client.host('api.nexmo.com')

    with pytest.raises(nexmo.NotFoundError) as excinfo:
        sms.send_message({'from': 'Vonage SMS API','to': '88888888888','text': 'Hello from Vonage'})
    excinfo.match(r"Resource not found")
    
    client.host('rest.nexmo.com')