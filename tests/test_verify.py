from util import *
from vonage.errors import VerifyError, BlockedNumberError


@responses.activate
def test_start_verification(verify, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/verify/json", 
        fixture_path="verify/start_verification.json")

    params = {"number": "447525856424", "brand": "MyApp"}

    response = verify.start_verification(params)
    assert isinstance(response, dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "number=447525856424" in request_body()
    assert "brand=MyApp" in request_body()
    assert response['status'] == '0'


@responses.activate
def test_start_verification_error(verify):
    stub(responses.POST, "https://api.nexmo.com/verify/json", 
        fixture_path="verify/start_verification_error.json")

    params = {"number": "447525856424", "brand": "MyApp"}

    with pytest.raises(VerifyError) as err:
        assert isinstance(verify.start_verification(params), dict)
        assert str(err.value) == 'Verify API method failed with error code 2: Your request is incomplete and missing the mandatory parameter `number`'


@responses.activate
def test_check_verification(verify, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/verify/check/json",
        fixture_path="verify/check_verification.json")

    assert isinstance(verify.check("8g88g88eg8g8gg9g90", code="123445"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "code=123445" in request_body()
    assert "request_id=8g88g88eg8g8gg9g90" in request_body()


@responses.activate
def test_check_verification_error(verify):
    stub(responses.POST, "https://api.nexmo.com/verify/check/json",
        fixture_path="verify/check_verification_error.json")

    with pytest.raises(VerifyError) as err:
        assert isinstance(verify.check("8g88g88eg8g8gg9g90", code="123445"), dict)
        assert str(err.value) == 'Verify.start_verification method failed with error code 16: The code inserted does not match the expected value'


@responses.activate
def test_search_for_verification(verify, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/verify/search/json",
        fixture_path="verify/search_verification.json")

    response = verify.search('xxx')
    assert isinstance(response, dict)
    assert response['status'] == 'IN PROGRESS'
    assert request_user_agent() == dummy_data.user_agent
    assert "request_id=xxx" in request_query()


@responses.activate
def test_search_for_verification_multiple(verify, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/verify/search/json",
        fixture_path="verify/search_verification.json")

    response = verify.search(request=['xxx', 'yyy'])
    assert isinstance(response, dict)
    assert response['status'] == 'IN PROGRESS'
    assert request_user_agent() == dummy_data.user_agent
    assert "request_ids=xxx&request_ids=yyy" in request_query()


@responses.activate
def test_search_for_verification_200_error(verify):
    stub(responses.GET, "https://api.nexmo.com/verify/search/json",
        fixture_path="verify/search_verification_200_error.json")
    
    with pytest.raises(VerifyError) as err:
        verify.search('xxx')
        assert str(err.value) == 'Verify API method failed with status: IN PROGRESS and error: No response found'


@responses.activate
def test_search_for_verification_error_no_id_provided(verify, dummy_data):
    stub(responses.GET, "https://api.nexmo.com/verify/search/json")
    
    with pytest.raises(VerifyError) as err:
        verify.search()
        assert str(err.value) == 'At least one request ID must be provided.'


@responses.activate
def test_cancel_verification(verify, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/verify/control/json",
        fixture_path='verify/cancel_verification.json')

    response = verify.cancel('asdf')
    assert isinstance(response, dict)
    assert response['command'] == 'cancel'
    assert request_user_agent() == dummy_data.user_agent
    assert "cmd=cancel" in request_body()
    assert "request_id=asdf" in request_body()


@responses.activate
def test_cancel_verification_error(verify, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/verify/control/json",
        fixture_path="verify/control_verification_error.json")

    with pytest.raises(VerifyError) as err:
        verify.cancel("asdf")
        assert str(err.value) == "Verify API method failed with status: 6 and error: The requestId 'asdf' does not exist or its no longer active."


@responses.activate
def test_trigger_next_verification_event(verify, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/verify/control/json",
        fixture_path='verify/trigger_next_event.json')

    response = verify.trigger_next_event("asdf")
    assert isinstance(response, dict)
    assert response['command'] == 'trigger_next_event'
    assert request_user_agent() == dummy_data.user_agent
    assert "cmd=trigger_next_event" in request_body()
    assert "request_id=asdf" in request_body()


@responses.activate
def test_trigger_next_verification_event_error(verify):
    stub(responses.POST, "https://api.nexmo.com/verify/control/json",
        fixture_path='verify/control_verification_error.json')

    with pytest.raises(VerifyError) as err:
        verify.trigger_next_event("asdf")
        assert str(err.value) == "Verify API method failed with status: 6 and error: The requestId 'asdf' does not exist or its no longer active."


@responses.activate
def test_start_verification_blacklisted_error_with_network_and_request_id(client, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/verify/json",
        fixture_path="verify/blocked_with_network_and_request_id.json"
    )

    params = {"number": "447525856424", "brand": "MyApp"}
    error_msg = "Error code 7: The number you are trying to verify is blocked for verification."
    
    with pytest.raises(BlockedNumberError, match=error_msg):
        response = client.verify.start_verification(params)
        assert request_user_agent() == dummy_data.user_agent
        assert "number=447525856424" in request_body()
        assert "brand=MyApp" in request_body()
        assert response["status"] == "7"
        assert response["network"] == "25503"
        assert response["request_id"] == "12345678"
        assert response["error_text"] == "The number you are trying to verify is blacklisted for verification"


@responses.activate
def test_start_psd2_verification(verify, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/verify/psd2/json",
        fixture_path='verify/start_verification.json')

    params = {"number": "447525856424", "brand": "MyApp"}

    assert isinstance(verify.psd2(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "number=447525856424" in request_body()
    assert "brand=MyApp" in request_body()


@responses.activate
def test_start_psd2_verification_error(verify, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/verify/psd2/json",
        fixture_path='verify/start_verification_error.json')

    params = {"brand": "MyApp"}

    with pytest.raises(VerifyError) as err:
        verify.psd2(params)
        assert str(err.value) == 'Verify API method failed with status: 2 and error: Your request is incomplete and missing the mandatory parameter `number`'


@responses.activate
def test_start_psd2_verification_blacklisted_error_with_network_and_request_id(client, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/verify/psd2/json",
        fixture_path="verify/blocked_with_network_and_request_id.json"
    )

    params = {"number": "447525856424", "brand": "MyApp"}
    
    with pytest.raises(BlockedNumberError) as err:
        client.verify.psd2(params)
        assert str(err.value) == 'Error code 7: The number you are trying to verify is blocked for verification.'
