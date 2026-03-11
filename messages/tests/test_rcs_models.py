import pytest
from vonage_messages.models import (
    RcsCustom,
    RcsFile,
    RcsImage,
    RcsResource,
    RcsText,
    RcsVideo,
)


def test_create_rcs_text():
    rcs_model = RcsText(
        to='1234567890',
        from_='asdf1234',
        text='Hello, World!',
    )
    rcs_dict = {
        'to': '1234567890',
        'from': 'asdf1234',
        'text': 'Hello, World!',
        'channel': 'rcs',
        'message_type': 'text',
    }

    assert rcs_model.model_dump(by_alias=True, exclude_none=True) == rcs_dict


def test_create_rcs_text_with_ampersand():
    """Tests that RCS from fields will allow an ampersand (&) character.

    See also: DEVX-10155
    """
    rcs_model = RcsText(
        to='1234567890',
        from_='Acme&SonsCo',
        text='Hello, World!',
    )
    rcs_dict = {
        'to': '1234567890',
        'from': 'Acme&SonsCo',
        'text': 'Hello, World!',
        'channel': 'rcs',
        'message_type': 'text',
    }

    assert rcs_model.model_dump(by_alias=True, exclude_none=True) == rcs_dict


def test_create_rcs_text_all_fields():
    rcs_model = RcsText(
        to='1234567890',
        from_='asdf1234',
        text='Hello, World!',
        client_ref='client-ref',
        webhook_url='https://example.com',
        ttl=600,
    )
    rcs_dict = {
        'to': '1234567890',
        'from': 'asdf1234',
        'text': 'Hello, World!',
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'ttl': 600,
        'channel': 'rcs',
        'message_type': 'text',
    }

    assert rcs_model.model_dump(by_alias=True, exclude_none=True) == rcs_dict


def test_create_rcs_image():
    rcs_model = RcsImage(
        to='1234567890',
        from_='asdf1234',
        image=RcsResource(
            url='https://example.com/image.jpg',
        ),
    )
    rcs_dict = {
        'to': '1234567890',
        'from': 'asdf1234',
        'image': {
            'url': 'https://example.com/image.jpg',
        },
        'channel': 'rcs',
        'message_type': 'image',
    }

    assert rcs_model.model_dump(by_alias=True, exclude_none=True) == rcs_dict


def test_create_rcs_video():
    rcs_model = RcsVideo(
        to='1234567890',
        from_='asdf1234',
        video=RcsResource(
            url='https://example.com/video.mp4',
        ),
    )
    rcs_dict = {
        'to': '1234567890',
        'from': 'asdf1234',
        'video': {
            'url': 'https://example.com/video.mp4',
        },
        'channel': 'rcs',
        'message_type': 'video',
    }

    assert rcs_model.model_dump(by_alias=True, exclude_none=True) == rcs_dict


def test_create_rcs_file():
    rcs_model = RcsFile(
        to='1234567890',
        from_='asdf1234',
        file=RcsResource(
            url='https://example.com/file.pdf',
        ),
    )
    rcs_dict = {
        'to': '1234567890',
        'from': 'asdf1234',
        'file': {
            'url': 'https://example.com/file.pdf',
        },
        'channel': 'rcs',
        'message_type': 'file',
    }

    assert rcs_model.model_dump(by_alias=True, exclude_none=True) == rcs_dict


def test_create_rcs_custom():
    rcs_model = RcsCustom(
        to='1234567890',
        from_='asdf1234',
        custom={'key': 'value'},
    )
    rcs_dict = {
        'to': '1234567890',
        'from': 'asdf1234',
        'custom': {'key': 'value'},
        'channel': 'rcs',
        'message_type': 'custom',
    }

    assert rcs_model.model_dump(by_alias=True, exclude_none=True) == rcs_dict

@pytest.mark.skip(reason="not yet implemented")
def test_rcs_suggestion_base():
    suggestion = RcsSuggestionBase(
        text='Reply',
        postback_data='postback-data',
    )
    suggestion_dict = {
        'text': 'Reply',
        'postback_data': 'postback-data',
    }

    assert suggestion.model_dump(by_alias=True, exclude_none=True) == suggestion_dict

@pytest.mark.skip(reason="not yet implemented")
def test_rcs_suggestion_base_without_text():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionBase(
            postback_data='postback-data',
        )
    assert "field required" in err.value.errors[0]['msg']

@pytest.mark.skip(reason="not yet implemented")
def test_rcs_suggestion_base_without_postback_data():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionBase(
            text='Reply',
        )
    assert "field required" in err.value.errors[0]['msg']

@pytest.mark.skip(reason="not yet implemented")
def test_rcs_suggestion_base_with_text_too_short():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionBase(
            text='',
            postback_data='postback-data',
        )
    assert "ensure this value has at least 1 characters" in err.value.errors[0]['msg']

@pytest.mark.skip(reason="not yet implemented")
def test_rcs_suggestion_base_with_text_too_long():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionBase(
            text='A' * 25 + 'B',
            postback_data='postback-data',
        )
    assert "ensure this value has at most 25 characters" in err.value.errors[0]['msg']