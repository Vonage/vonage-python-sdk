from util import *


@responses.activate
def test_initiate_call(voice, dummy_data):
    stub(responses.POST, "https://rest.nexmo.com/call/json")

    params = {"to": "16365553226", "answer_url": "http://example.com/answer"}

    assert isinstance(voice.initiate_call(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "to=16365553226" in request_body()
    assert "answer_url=http%3A%2F%2Fexample.com%2Fanswer" in request_body()


@responses.activate
def test_initiate_tts_call(voice, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/tts/json")

    params = {"to": "16365553226", "text": "Hello"}

    assert isinstance(voice.initiate_tts_call(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "to=16365553226" in request_body()
    assert "text=Hello" in request_body()


@responses.activate
def test_initiate_tts_prompt_call(voice, dummy_data):
    stub(responses.POST, "https://api.nexmo.com/tts-prompt/json")

    params = {
        "to": "16365553226",
        "text": "Hello",
        "max_digits": 4,
        "bye_text": "Goodbye",
    }

    assert isinstance(voice.initiate_tts_prompt_call(params), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "to=16365553226" in request_body()
    assert "text=Hello" in request_body()
    assert "max_digits=4" in request_body()
    assert "bye_text=Goodbye" in request_body()
