from vonage import PayPrompts

import pytest
from pydantic import ValidationError


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
        errors={
            'InvalidCardType': {
                'text': 'The card you are trying to use is not valid for this purchase.'
            }
        },
    )
    assert type(text_prompt) == PayPrompts.TextPrompt


def test_create_text_model_from_dict():
    text_dict = {
        'type': 'CardNumber',
        'text': 'Enter your card number.',
        'errors': {
            'InvalidCardType': {
                'text': 'The card you are trying to use is not valid for this purchase.'
            }
        },
    }
    text_prompt = PayPrompts.create_text_model(text_dict)
    assert type(text_prompt) == PayPrompts.TextPrompt


def test_error_message_not_in_subdictionary():
    with pytest.raises(ValidationError):
        PayPrompts.TextPrompt(
            type='CardNumber',
            text='Enter your card number.',
            errors={
                'InvalidCardType': 'The card you are trying to use is not valid for this purchase.'
            },
        )


def test_invalid_error_type_for_prompt():
    with pytest.raises(ValueError) as err:
        PayPrompts.TextPrompt(
            type='SecurityCode',
            text='Enter your card number.',
            errors={
                'InvalidCardType': {
                    'text': 'The card you are trying to use is not valid for this purchase.'
                }
            },
        )

    assert (
        'Value "InvalidCardType" is not a valid error for the "SecurityCode" prompt type.'
        in str(err.value)
    )
