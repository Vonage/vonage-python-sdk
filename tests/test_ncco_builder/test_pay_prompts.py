from vonage import PayPrompts


def test_create_voice_model():
    voice_prompt = PayPrompts.VoicePrompt(language='en-GB', style=1)
    assert (type(voice_prompt)) == PayPrompts.VoicePrompt


def test_create_voice_model_from_dict():
    voice_dict = {'language': 'en-GB', 'style': 1}
    voice_prompt = PayPrompts.create_voice_model(voice_dict)
    assert (type(voice_prompt)) == PayPrompts.VoicePrompt


def test_create_text_model():
    text_prompt = PayPrompts.TextPrompt(
        type='CardNumber',
        text='Enter your card number.',
        errors={'InvalidCardType': {'text': 'The card you are trying to use is not valid for this purchase.'}},
    )
    assert type(text_prompt) == PayPrompts.TextPrompt


def test_create_text_model_from_dict():
    text_dict = {
        'type': 'CardNumber',
        'text': 'Enter your card number.',
        'errors': {'InvalidCardType': {'text': 'The card you are trying to use is not valid for this purchase.'}},
    }
    text_prompt = PayPrompts.create_text_model(text_dict)
    assert type(text_prompt) == PayPrompts.TextPrompt


def test_pay_text_field_not_present():
    assert 0


def test_pay_text_invalid_error_value():
    assert 0
