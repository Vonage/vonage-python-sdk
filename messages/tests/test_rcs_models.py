import pytest
from pydantic import ValidationError
from vonage_messages.models import (
    RcsCardBase,
    RcsCardItem,
    RcsCardMessage,
    RcsCarousel,
    RcsCustom,
    RcsFile,
    RcsImage,
    RcsOptions,
    RcsOptionsCard,
    RcsOptionsCarousel,
    RcsResource,
    RcsSuggestionActionCreateCalendarEvent,
    RcsSuggestionActionDial,
    RcsSuggestionActionOpenUrl,
    RcsSuggestionActionOpenUrlWebview,
    RcsSuggestionActionShareLocation,
    RcsSuggestionActionViewLocation,
    RcsSuggestionBase,
    RcsSuggestionReply,
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
        rcs=RcsOptions(
            category='transaction',
        ),
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
        'rcs': {
            'category': 'transaction',
        },
    }

    assert rcs_model.model_dump(by_alias=True, exclude_none=True) == rcs_dict


def test_create_rcs_text_with_suggestions():
    rcs_model = RcsText(
        to='1234567890',
        from_='asdf1234',
        text='Hello, World!',
        suggestions=[
            RcsSuggestionReply(
                text='Reply',
                postback_data='postback-data',
            ),
            RcsSuggestionActionDial(
                text='Call us',
                postback_data='postback-data',
                phone_number='447900000000',
            ),
        ],
    )
    rcs_dict = {
        'to': '1234567890',
        'from': 'asdf1234',
        'text': 'Hello, World!',
        'suggestions': [
            {
                'type': 'reply',
                'text': 'Reply',
                'postback_data': 'postback-data',
            },
            {
                'type': 'dial',
                'text': 'Call us',
                'postback_data': 'postback-data',
                'phone_number': '447900000000',
            },
        ],
        'channel': 'rcs',
        'message_type': 'text',
    }

    assert rcs_model.model_dump(by_alias=True, exclude_none=True) == rcs_dict


def test_create_rcs_text_with_all_suggestion_types():
    rcs_model = RcsText(
        to='1234567890',
        from_='asdf1234',
        text='Hello, World!',
        suggestions=[
            RcsSuggestionReply(
                text='Reply',
                postback_data='postback-data',
            ),
            RcsSuggestionActionDial(
                text='Call us',
                postback_data='postback-data',
                phone_number='447900000000',
            ),
            RcsSuggestionActionViewLocation(
                text='View location',
                postback_data='postback-data',
                latitude='51.5074',
                longitude='-0.1278',
                pin_label='London',
                fallback_url='https://example.com/location',
            ),
            RcsSuggestionActionShareLocation(
                text='Share location',
                postback_data='postback-data',
            ),
            RcsSuggestionActionOpenUrl(
                text='Open URL',
                postback_data='postback-data',
                url='https://example.com',
                description='Click to open the URL',
            ),
            RcsSuggestionActionOpenUrlWebview(
                text='Open URL in webview',
                postback_data='postback-data',
                url='https://example.com',
                description='Click to open the URL in a webview',
                view_mode='FULL',
            ),
            RcsSuggestionActionCreateCalendarEvent(
                text='Add to calendar',
                postback_data='postback-data',
                start_time='2024-01-01T12:00:00Z',
                end_time='2024-01-01T13:00:00Z',
                title='Meeting with Bob',
                description='Discuss project updates',
                fallback_url='https://example.com/calendar-event',
            ),
        ],
    )
    rcs_dict = {
        'to': '1234567890',
        'from': 'asdf1234',
        'text': 'Hello, World!',
        'suggestions': [
            {
                'type': 'reply',
                'text': 'Reply',
                'postback_data': 'postback-data',
            },
            {
                'type': 'dial',
                'text': 'Call us',
                'postback_data': 'postback-data',
                'phone_number': '447900000000',
            },
            {
                'type': 'view_location',
                'text': 'View location',
                'postback_data': 'postback-data',
                'latitude': '51.5074',
                'longitude': '-0.1278',
                'pin_label': 'London',
                'fallback_url': 'https://example.com/location',
            },
            {
                'type': 'share_location',
                'text': 'Share location',
                'postback_data': 'postback-data',
            },
            {
                'type': 'open_url',
                'text': 'Open URL',
                'postback_data': 'postback-data',
                'url': 'https://example.com',
                'description': 'Click to open the URL',
            },
            {
                'type': 'open_url_in_webview',
                'text': 'Open URL in webview',
                'postback_data': 'postback-data',
                'url': 'https://example.com',
                'description': 'Click to open the URL in a webview',
                'view_mode': 'FULL',
            },
            {
                'type': 'create_calendar_event',
                'text': 'Add to calendar',
                'postback_data': 'postback-data',
                'start_time': '2024-01-01T12:00:00Z',
                'end_time': '2024-01-01T13:00:00Z',
                'title': 'Meeting with Bob',
                'description': 'Discuss project updates',
                'fallback_url': 'https://example.com/calendar-event',
            },
        ],
        'channel': 'rcs',
        'message_type': 'text',
    }

    assert rcs_model.model_dump(by_alias=True, exclude_none=True) == rcs_dict


def test_create_rcs_text_with_insuffient_suggestions():
    with pytest.raises(ValidationError) as err:
        rcs_model = RcsText(
            to='1234567890',
            from_='asdf1234',
            text='Hello, World!',
            suggestions=[],
        )
    assert "List should have at least 1 item" in str(err.value)


def test_create_rcs_text_with_too_many_suggestions():
    with pytest.raises(ValidationError) as err:
        rcs_model = RcsText(
            to='1234567890',
            from_='asdf1234',
            text='Hello, World!',
            suggestions=[
                RcsSuggestionReply(
                    text='Reply',
                    postback_data='postback-data',
                ),
            ]
            * 12,
        )
    assert "List should have at most 11 items" in str(err.value)


def test_create_rcs_text_with_inavalid_suggestion_types():
    with pytest.raises(ValidationError) as err:
        rcs_model = RcsText(
            to='1234567890',
            from_='asdf1234',
            text='Hello, World!',
            suggestions=[
                RcsSuggestionReply(
                    text='Reply',
                    postback_data='postback-data',
                ),
                "Invalid suggestion type",
            ],
        )
    assert "Input should be a valid dictionary or instance" in str(err.value)


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


def test_create_rcs_card_base():
    card_base = RcsCardBase(
        title='Card title',
        text='Card description',
        media_url='https://example.com/image.jpg',
    )
    card_base_dict = {
        'title': 'Card title',
        'text': 'Card description',
        'media_url': 'https://example.com/image.jpg',
    }
    assert card_base.model_dump(by_alias=True, exclude_none=True) == card_base_dict


def test_create_rcs_card_base_with_optional_params():
    card_base = RcsCardBase(
        title='Card title',
        text='Card description',
        media_url='https://example.com/image.jpg',
        media_description='Image description',
        media_height='MEDIUM',
        thumbnail_url='https://example.com/thumbnail.jpg',
        media_force_refresh=True,
    )
    card_base_dict = {
        'title': 'Card title',
        'text': 'Card description',
        'media_url': 'https://example.com/image.jpg',
        'media_description': 'Image description',
        'media_height': 'MEDIUM',
        'thumbnail_url': 'https://example.com/thumbnail.jpg',
        'media_force_refresh': True,
    }
    assert card_base.model_dump(by_alias=True, exclude_none=True) == card_base_dict


def test_create_rcs_card_base_with_suggestions():
    card_base = RcsCardBase(
        title='Card title',
        text='Card description',
        media_url='https://example.com/image.jpg',
        suggestions=[
            RcsSuggestionReply(
                text='Reply',
                postback_data='postback-data',
            ),
            RcsSuggestionActionDial(
                text='Call us',
                postback_data='postback-data',
                phone_number='447900000000',
            ),
        ],
    )
    card_base_dict = {
        'title': 'Card title',
        'text': 'Card description',
        'media_url': 'https://example.com/image.jpg',
        'suggestions': [
            {
                'type': 'reply',
                'text': 'Reply',
                'postback_data': 'postback-data',
            },
            {
                'type': 'dial',
                'text': 'Call us',
                'postback_data': 'postback-data',
                'phone_number': '447900000000',
            },
        ],
    }
    assert card_base.model_dump(by_alias=True, exclude_none=True) == card_base_dict


def test_create_rcs_card_base_with_all_suggestion_types():
    card_base_1 = RcsCardBase(
        title='Card title',
        text='Card description',
        media_url='https://example.com/image.jpg',
        suggestions=[
            RcsSuggestionReply(
                text='Reply',
                postback_data='postback-data',
            ),
            RcsSuggestionActionDial(
                text='Call us',
                postback_data='postback-data',
                phone_number='447900000000',
            ),
            RcsSuggestionActionViewLocation(
                text='View location',
                postback_data='postback-data',
                latitude='51.5074',
                longitude='-0.1278',
                pin_label='London',
                fallback_url='https://example.com/location',
            ),
            RcsSuggestionActionShareLocation(
                text='Share location',
                postback_data='postback-data',
            ),
        ],
    )
    card_base_2 = RcsCardBase(
        title='Card title',
        text='Card description',
        media_url='https://example.com/image.jpg',
        suggestions=[
            RcsSuggestionActionOpenUrl(
                text='Open URL',
                postback_data='postback-data',
                url='https://example.com',
                description='Click to open the URL',
            ),
            RcsSuggestionActionOpenUrlWebview(
                text='Open URL in webview',
                postback_data='postback-data',
                url='https://example.com',
                description='Click to open the URL in a webview',
                view_mode='FULL',
            ),
            RcsSuggestionActionCreateCalendarEvent(
                text='Add to calendar',
                postback_data='postback-data',
                start_time='2024-01-01T12:00:00Z',
                end_time='2024-01-01T13:00:00Z',
                title='Meeting with Bob',
                description='Discuss project updates',
                fallback_url='https://example.com/calendar-event',
            ),
        ],
    )
    card_base_dict_1 = {
        'title': 'Card title',
        'text': 'Card description',
        'media_url': 'https://example.com/image.jpg',
        'suggestions': [
            {
                'type': 'reply',
                'text': 'Reply',
                'postback_data': 'postback-data',
            },
            {
                'type': 'dial',
                'text': 'Call us',
                'postback_data': 'postback-data',
                'phone_number': '447900000000',
            },
            {
                'type': 'view_location',
                'text': 'View location',
                'postback_data': 'postback-data',
                'latitude': '51.5074',
                'longitude': '-0.1278',
                'pin_label': 'London',
                'fallback_url': 'https://example.com/location',
            },
            {
                'type': 'share_location',
                'text': 'Share location',
                'postback_data': 'postback-data',
            },
        ],
    }
    card_base_dict_2 = {
        'title': 'Card title',
        'text': 'Card description',
        'media_url': 'https://example.com/image.jpg',
        'suggestions': [
            {
                'type': 'open_url',
                'text': 'Open URL',
                'postback_data': 'postback-data',
                'url': 'https://example.com',
                'description': 'Click to open the URL',
            },
            {
                'type': 'open_url_in_webview',
                'text': 'Open URL in webview',
                'postback_data': 'postback-data',
                'url': 'https://example.com',
                'description': 'Click to open the URL in a webview',
                'view_mode': 'FULL',
            },
            {
                'type': 'create_calendar_event',
                'text': 'Add to calendar',
                'postback_data': 'postback-data',
                'start_time': '2024-01-01T12:00:00Z',
                'end_time': '2024-01-01T13:00:00Z',
                'title': 'Meeting with Bob',
                'description': 'Discuss project updates',
                'fallback_url': 'https://example.com/calendar-event',
            },
        ],
    }
    assert card_base_1.model_dump(by_alias=True, exclude_none=True) == card_base_dict_1
    assert card_base_2.model_dump(by_alias=True, exclude_none=True) == card_base_dict_2


def test_create_rcs_card_base_without_title():
    with pytest.raises(ValidationError) as err:
        card_base = RcsCardBase(
            text='Card description',
            media_url='https://example.com/image.jpg',
        )
    assert "Field required" in str(err.value)


def test_create_rcs_card_base_without_text():
    with pytest.raises(ValidationError) as err:
        card_base = RcsCardBase(
            title='Card title',
            media_url='https://example.com/image.jpg',
        )
    assert "Field required" in str(err.value)


def test_create_rcs_card_base_without_media_url():
    with pytest.raises(ValidationError) as err:
        card_base = RcsCardBase(
            title='Card title',
            text='Card description',
        )
    assert "Field required" in str(err.value)


def test_create_rcs_card_base_with_title_too_short():
    with pytest.raises(ValidationError) as err:
        card_base = RcsCardBase(
            title='',
            text='Card description',
            media_url='https://example.com/image.jpg',
        )
    assert "String should have at least 1 character" in str(err.value)


def test_create_rcs_card_base_with_title_too_long():
    with pytest.raises(ValidationError) as err:
        card_base = RcsCardBase(
            title='A' * 200 + 'B',
            text='Card description',
            media_url='https://example.com/image.jpg',
        )
    assert "String should have at most 200 characters" in str(err.value)


def test_create_rcs_card_base_with_text_too_short():
    with pytest.raises(ValidationError) as err:
        card_base = RcsCardBase(
            to='1234567890',
            from_='asdf1234',
            title='Card title',
            text='',
            media_url='https://example.com/image.jpg',
        )
    assert "String should have at least 1 character" in str(err.value)


def test_create_rcs_card_base_with_text_too_long():
    with pytest.raises(ValidationError) as err:
        card_base = RcsCardBase(
            to='1234567890',
            from_='asdf1234',
            title='Card title',
            text='A' * 2000 + 'B',
            media_url='https://example.com/image.jpg',
        )
    assert "String should have at most 2000 characters" in str(err.value)


def test_create_rcs_card_base_with_insuffient_suggestions():
    with pytest.raises(ValidationError) as err:
        card_base = RcsCardBase(
            title='Card title',
            text='Card description',
            media_url='https://example.com/image.jpg',
            suggestions=[],
        )
    assert "List should have at least 1 item" in str(err.value)


def test_create_rcs_card_base_with_too_many_suggestions():
    with pytest.raises(ValidationError) as err:
        card_base = RcsCardBase(
            title='Card title',
            text='Card description',
            media_url='https://example.com/image.jpg',
            suggestions=[
                RcsSuggestionReply(
                    text='Reply',
                    postback_data='postback-data',
                ),
            ]
            * 5,
        )
    assert "List should have at most 4 items" in str(err.value)


def test_create_rcs_card_base_with_inavalid_suggestion_types():
    with pytest.raises(ValidationError) as err:
        card_base = RcsCardBase(
            title='Card title',
            text='Card description',
            media_url='https://example.com/image.jpg',
            suggestions=[
                RcsSuggestionReply(
                    text='Reply',
                    postback_data='postback-data',
                ),
                "Invalid suggestion type",
            ],
        )
    assert "Input should be a valid dictionary or instance" in str(err.value)


def test_create_rcs_card_message():
    card = RcsCardMessage(
        to='1234567890',
        from_='asdf1234',
        title='Card title',
        text='Card description',
        media_url='https://example.com/image.jpg',
    )
    card_dict = {
        'to': '1234567890',
        'from': 'asdf1234',
        'title': 'Card title',
        'text': 'Card description',
        'media_url': 'https://example.com/image.jpg',
        'channel': 'rcs',
        'message_type': 'card',
    }
    assert card.model_dump(by_alias=True, exclude_none=True) == card_dict


def test_create_rcs_card_message_with_optional_params():
    card = RcsCardMessage(
        to='1234567890',
        from_='asdf1234',
        title='Card title',
        text='Card description',
        media_url='https://example.com/image.jpg',
        media_description='Image description',
        media_height='MEDIUM',
        thumbnail_url='https://example.com/thumbnail.jpg',
        media_force_refresh=True,
        rcs=RcsOptionsCard(
            card_orientation='VERTICAL',
            image_alignment='LEFT',
        ),
    )
    card_dict = {
        'to': '1234567890',
        'from': 'asdf1234',
        'title': 'Card title',
        'text': 'Card description',
        'media_url': 'https://example.com/image.jpg',
        'media_description': 'Image description',
        'media_height': 'MEDIUM',
        'thumbnail_url': 'https://example.com/thumbnail.jpg',
        'media_force_refresh': True,
        'rcs': {
            'card_orientation': 'VERTICAL',
            'image_alignment': 'LEFT',
        },
        'channel': 'rcs',
        'message_type': 'card',
    }
    assert card.model_dump(by_alias=True, exclude_none=True) == card_dict


def test_create_rcs_card_message_with_suggestions():
    card = RcsCardMessage(
        to='1234567890',
        from_='asdf1234',
        title='Card title',
        text='Card description',
        media_url='https://example.com/image.jpg',
        suggestions=[
            RcsSuggestionReply(
                text='Reply',
                postback_data='postback-data',
            ),
            RcsSuggestionActionDial(
                text='Call us',
                postback_data='postback-data',
                phone_number='447900000000',
            ),
        ],
    )
    card_dict = {
        'to': '1234567890',
        'from': 'asdf1234',
        'title': 'Card title',
        'text': 'Card description',
        'media_url': 'https://example.com/image.jpg',
        'suggestions': [
            {
                'type': 'reply',
                'text': 'Reply',
                'postback_data': 'postback-data',
            },
            {
                'type': 'dial',
                'text': 'Call us',
                'postback_data': 'postback-data',
                'phone_number': '447900000000',
            },
        ],
        'channel': 'rcs',
        'message_type': 'card',
    }
    assert card.model_dump(by_alias=True, exclude_none=True) == card_dict


def test_create_rcs_card_message_without_title():
    with pytest.raises(ValidationError) as err:
        card = RcsCardMessage(
            to='1234567890',
            from_='asdf1234',
            text='Card description',
            media_url='https://example.com/image.jpg',
        )
    assert "Field required" in str(err.value)


def test_create_rcs_card_message_without_text():
    with pytest.raises(ValidationError) as err:
        card = RcsCardMessage(
            to='1234567890',
            from_='asdf1234',
            title='Card title',
            media_url='https://example.com/image.jpg',
        )
    assert "Field required" in str(err.value)


def test_create_rcs_card_message_without_media_url():
    with pytest.raises(ValidationError) as err:
        card = RcsCardMessage(
            to='1234567890',
            from_='asdf1234',
            title='Card title',
            text='Card description',
        )
    assert "Field required" in str(err.value)


def test_create_rcs_card_message_with_title_too_short():
    with pytest.raises(ValidationError) as err:
        card = RcsCardMessage(
            to='1234567890',
            from_='asdf1234',
            title='',
            text='Card description',
            media_url='https://example.com/image.jpg',
        )
    assert "String should have at least 1 character" in str(err.value)


def test_create_rcs_card_message_with_title_too_long():
    with pytest.raises(ValidationError) as err:
        card = RcsCardMessage(
            to='1234567890',
            from_='asdf1234',
            title='A' * 200 + 'B',
            text='Card description',
            media_url='https://example.com/image.jpg',
        )
    assert "String should have at most 200 characters" in str(err.value)


def test_create_rcs_card_message_with_text_too_short():
    with pytest.raises(ValidationError) as err:
        card = RcsCardMessage(
            to='1234567890',
            from_='asdf1234',
            title='Card title',
            text='',
            media_url='https://example.com/image.jpg',
        )
    assert "String should have at least 1 character" in str(err.value)


def test_create_rcs_card_message_with_text_too_long():
    with pytest.raises(ValidationError) as err:
        card = RcsCardMessage(
            to='1234567890',
            from_='asdf1234',
            title='Card title',
            text='A' * 2000 + 'B',
            media_url='https://example.com/image.jpg',
        )
    assert "String should have at most 2000 characters" in str(err.value)


def test_create_rcs_card_message_with_insuffient_suggestions():
    with pytest.raises(ValidationError) as err:
        card = RcsCardMessage(
            to='1234567890',
            from_='asdf1234',
            title='Card title',
            text='Card description',
            media_url='https://example.com/image.jpg',
            suggestions=[],
        )
    assert "List should have at least 1 item" in str(err.value)


def test_create_rcs_card_message_with_too_many_suggestions():
    with pytest.raises(ValidationError) as err:
        card = RcsCardMessage(
            to='1234567890',
            from_='asdf1234',
            title='Card title',
            text='Card description',
            media_url='https://example.com/image.jpg',
            suggestions=[
                RcsSuggestionReply(
                    text='Reply',
                    postback_data='postback-data',
                ),
            ]
            * 5,
        )
    assert "List should have at most 4 items" in str(err.value)


def test_create_rcs_card_message_with_inavalid_suggestion_types():
    with pytest.raises(ValidationError) as err:
        card = RcsCardMessage(
            to='1234567890',
            from_='asdf1234',
            title='Card title',
            text='Card description',
            media_url='https://example.com/image.jpg',
            suggestions=[
                RcsSuggestionReply(
                    text='Reply',
                    postback_data='postback-data',
                ),
                "Invalid suggestion type",
            ],
        )
    assert "Input should be a valid dictionary or instance" in str(err.value)


def test_create_rcs_card_item():
    card_content = RcsCardItem(
        title='Card title',
        text='Card description',
        media_url='https://example.com/image.jpg',
        media_height='MEDIUM',
    )
    card_item_dict = {
        'title': 'Card title',
        'text': 'Card description',
        'media_url': 'https://example.com/image.jpg',
        'media_height': 'MEDIUM',
    }
    assert card_content.model_dump(by_alias=True, exclude_none=True) == card_item_dict


def test_create_rcs_card_item_with_optional_params():
    card_content = RcsCardItem(
        title='Card title',
        text='Card description',
        media_url='https://example.com/image.jpg',
        media_description='Image description',
        media_height='MEDIUM',
        thumbnail_url='https://example.com/thumbnail.jpg',
        media_force_refresh=True,
    )
    card_item_dict = {
        'title': 'Card title',
        'text': 'Card description',
        'media_url': 'https://example.com/image.jpg',
        'media_description': 'Image description',
        'media_height': 'MEDIUM',
        'thumbnail_url': 'https://example.com/thumbnail.jpg',
        'media_force_refresh': True,
    }
    assert card_content.model_dump(by_alias=True, exclude_none=True) == card_item_dict


def test_create_rcs_card_item_with_suggestions():
    card_content = RcsCardItem(
        title='Card title',
        text='Card description',
        media_url='https://example.com/image.jpg',
        media_height='MEDIUM',
        suggestions=[
            RcsSuggestionReply(
                text='Reply',
                postback_data='postback-data',
            ),
            RcsSuggestionActionDial(
                text='Call us',
                postback_data='postback-data',
                phone_number='447900000000',
            ),
        ],
    )
    card_item_dict = {
        'title': 'Card title',
        'text': 'Card description',
        'media_url': 'https://example.com/image.jpg',
        'media_height': 'MEDIUM',
        'suggestions': [
            {
                'type': 'reply',
                'text': 'Reply',
                'postback_data': 'postback-data',
            },
            {
                'type': 'dial',
                'text': 'Call us',
                'postback_data': 'postback-data',
                'phone_number': '447900000000',
            },
        ],
    }
    assert card_content.model_dump(by_alias=True, exclude_none=True) == card_item_dict


def test_create_rcs_card_item_without_title():
    with pytest.raises(ValidationError) as err:
        card = RcsCardItem(
            text='Card description',
            media_url='https://example.com/image.jpg',
        )
    assert "Field required" in str(err.value)


def test_create_rcs_card_item_without_text():
    with pytest.raises(ValidationError) as err:
        card = RcsCardItem(
            title='Card title',
            media_url='https://example.com/image.jpg',
        )
    assert "Field required" in str(err.value)


def test_create_rcs_card_item_without_media_url():
    with pytest.raises(ValidationError) as err:
        card = RcsCardItem(
            title='Card title',
            text='Card description',
        )
    assert "Field required" in str(err.value)


def test_create_rcs_card_item_without_media_height():
    with pytest.raises(ValidationError) as err:
        card = RcsCardItem(
            title='Card title',
            text='Card description',
            media_url='https://example.com/image.jpg',
        )
    assert "Field required" in str(err.value)


def test_create_rcs_card_item_with_title_too_short():
    with pytest.raises(ValidationError) as err:
        card = RcsCardItem(
            title='',
            text='Card description',
            media_url='https://example.com/image.jpg',
        )
    assert "String should have at least 1 character" in str(err.value)


def test_create_rcs_card_item_with_title_too_long():
    with pytest.raises(ValidationError) as err:
        card = RcsCardItem(
            title='A' * 200 + 'B',
            text='Card description',
            media_url='https://example.com/image.jpg',
        )
    assert "String should have at most 200 characters" in str(err.value)


def test_create_rcs_card_item_with_text_too_short():
    with pytest.raises(ValidationError) as err:
        card = RcsCardItem(
            title='Card title',
            text='',
            media_url='https://example.com/image.jpg',
        )
    assert "String should have at least 1 character" in str(err.value)


def test_create_rcs_card_item_with_text_too_long():
    with pytest.raises(ValidationError) as err:
        card = RcsCardItem(
            title='Card title',
            text='A' * 2000 + 'B',
            media_url='https://example.com/image.jpg',
        )
    assert "String should have at most 2000 characters" in str(err.value)


def test_create_rcs_card_item_with_insuffient_suggestions():
    with pytest.raises(ValidationError) as err:
        card = RcsCardItem(
            title='Card title',
            text='Card description',
            media_url='https://example.com/image.jpg',
            suggestions=[],
        )
    assert "List should have at least 1 item" in str(err.value)


def test_create_rcs_card_item_with_too_many_suggestions():
    with pytest.raises(ValidationError) as err:
        card = RcsCardItem(
            title='Card title',
            text='Card description',
            media_url='https://example.com/image.jpg',
            suggestions=[
                RcsSuggestionReply(
                    text='Reply',
                    postback_data='postback-data',
                ),
            ]
            * 5,
        )
    assert "List should have at most 4 items" in str(err.value)


def test_create_rcs_card_item_with_inavalid_suggestion_types():
    with pytest.raises(ValidationError) as err:
        card = RcsCardItem(
            title='Card title',
            text='Card description',
            media_url='https://example.com/image.jpg',
            suggestions=[
                RcsSuggestionReply(
                    text='Reply',
                    postback_data='postback-data',
                ),
                "Invalid suggestion type",
            ],
        )
    assert "Input should be a valid dictionary or instance" in str(err.value)


def test_create_rcs_carousel():
    carousel = RcsCarousel(
        to='1234567890',
        from_='asdf1234',
        cards=[
            RcsCardItem(
                title='Card title',
                text='Card description',
                media_url='https://example.com/image.jpg',
                media_height='MEDIUM',
            )
        ]
        * 2,
        rcs=RcsOptionsCarousel(
            card_width='MEDIUM',
        ),
    )
    carousel_dict = {
        'to': '1234567890',
        'from': 'asdf1234',
        'cards': [
            {
                'title': 'Card title',
                'text': 'Card description',
                'media_url': 'https://example.com/image.jpg',
                'media_height': 'MEDIUM',
            }
        ]
        * 2,
        'rcs': {
            'card_width': 'MEDIUM',
        },
        'channel': 'rcs',
        'message_type': 'carousel',
    }
    assert carousel.model_dump(by_alias=True, exclude_none=True) == carousel_dict


def test_create_rcs_carousel_with_optional_params():
    carousel = RcsCarousel(
        to='1234567890',
        from_='asdf1234',
        cards=[
            RcsCardItem(
                title='Card title',
                text='Card description',
                media_url='https://example.com/image.jpg',
                media_description='Image description',
                media_height='MEDIUM',
                thumbnail_url='https://example.com/thumbnail.jpg',
                media_force_refresh=True,
            )
        ]
        * 2,
        rcs=RcsOptionsCarousel(
            card_width='MEDIUM',
        ),
    )
    carousel_dict = {
        'to': '1234567890',
        'from': 'asdf1234',
        'cards': [
            {
                'title': 'Card title',
                'text': 'Card description',
                'media_url': 'https://example.com/image.jpg',
                'media_description': 'Image description',
                'media_height': 'MEDIUM',
                'thumbnail_url': 'https://example.com/thumbnail.jpg',
                'media_force_refresh': True,
            }
        ]
        * 2,
        'rcs': {
            'card_width': 'MEDIUM',
        },
        'channel': 'rcs',
        'message_type': 'carousel',
    }
    assert carousel.model_dump(by_alias=True, exclude_none=True) == carousel_dict


def test_create_rcs_carousel_with_suggestions():
    carousel = RcsCarousel(
        to='1234567890',
        from_='asdf1234',
        cards=[
            RcsCardItem(
                title='Card title',
                text='Card description',
                media_url='https://example.com/image.jpg',
                media_height='MEDIUM',
            )
        ]
        * 2,
        suggestions=[
            RcsSuggestionReply(
                text='Reply',
                postback_data='postback-data',
            ),
            RcsSuggestionActionDial(
                text='Call us',
                postback_data='postback-data',
                phone_number='447900000000',
            ),
        ],
        rcs=RcsOptionsCarousel(
            card_width='MEDIUM',
        ),
    )
    carousel_dict = {
        'to': '1234567890',
        'from': 'asdf1234',
        'cards': [
            {
                'title': 'Card title',
                'text': 'Card description',
                'media_url': 'https://example.com/image.jpg',
                'media_height': 'MEDIUM',
            }
        ]
        * 2,
        'suggestions': [
            {
                'type': 'reply',
                'text': 'Reply',
                'postback_data': 'postback-data',
            },
            {
                'type': 'dial',
                'text': 'Call us',
                'postback_data': 'postback-data',
                'phone_number': '447900000000',
            },
        ],
        'rcs': {
            'card_width': 'MEDIUM',
        },
        'channel': 'rcs',
        'message_type': 'carousel',
    }
    assert carousel.model_dump(by_alias=True, exclude_none=True) == carousel_dict


def test_create_rcs_carousel_with_all_suggestion_types():
    carousel = RcsCarousel(
        to='1234567890',
        from_='asdf1234',
        cards=[
            RcsCardItem(
                title='Card title',
                text='Card description',
                media_url='https://example.com/image.jpg',
                media_height='MEDIUM',
            )
        ]
        * 2,
        suggestions=[
            RcsSuggestionReply(
                text='Reply',
                postback_data='postback-data',
            ),
            RcsSuggestionActionDial(
                text='Call us',
                postback_data='postback-data',
                phone_number='447900000000',
            ),
            RcsSuggestionActionViewLocation(
                text='View location',
                postback_data='postback-data',
                latitude='51.5074',
                longitude='-0.1278',
                pin_label='London',
                fallback_url='https://example.com/location',
            ),
            RcsSuggestionActionShareLocation(
                text='Share location',
                postback_data='postback-data',
            ),
            RcsSuggestionActionOpenUrl(
                text='Open URL',
                postback_data='postback-data',
                url='https://example.com',
                description='Click to open the URL',
            ),
            RcsSuggestionActionOpenUrlWebview(
                text='Open URL in webview',
                postback_data='postback-data',
                url='https://example.com',
                description='Click to open the URL in a webview',
                view_mode='FULL',
            ),
            RcsSuggestionActionCreateCalendarEvent(
                text='Add to calendar',
                postback_data='postback-data',
                start_time='2024-01-01T12:00:00Z',
                end_time='2024-01-01T13:00:00Z',
                title='Meeting with Bob',
                description='Discuss project updates',
                fallback_url='https://example.com/calendar-event',
            ),
        ],
        rcs=RcsOptionsCarousel(
            card_width='MEDIUM',
        ),
    )
    carousel_dict = {
        'to': '1234567890',
        'from': 'asdf1234',
        'cards': [
            {
                'title': 'Card title',
                'text': 'Card description',
                'media_url': 'https://example.com/image.jpg',
                'media_height': 'MEDIUM',
            }
        ]
        * 2,
        'suggestions': [
            {
                'type': 'reply',
                'text': 'Reply',
                'postback_data': 'postback-data',
            },
            {
                'type': 'dial',
                'text': 'Call us',
                'postback_data': 'postback-data',
                'phone_number': '447900000000',
            },
            {
                'type': 'view_location',
                'text': 'View location',
                'postback_data': 'postback-data',
                'latitude': '51.5074',
                'longitude': '-0.1278',
                'pin_label': 'London',
                'fallback_url': 'https://example.com/location',
            },
            {
                'type': 'share_location',
                'text': 'Share location',
                'postback_data': 'postback-data',
            },
            {
                'type': 'open_url',
                'text': 'Open URL',
                'postback_data': 'postback-data',
                'url': 'https://example.com',
                'description': 'Click to open the URL',
            },
            {
                'type': 'open_url_in_webview',
                'text': 'Open URL in webview',
                'postback_data': 'postback-data',
                'url': 'https://example.com',
                'description': 'Click to open the URL in a webview',
                'view_mode': 'FULL',
            },
            {
                'type': 'create_calendar_event',
                'text': 'Add to calendar',
                'postback_data': 'postback-data',
                'start_time': '2024-01-01T12:00:00Z',
                'end_time': '2024-01-01T13:00:00Z',
                'title': 'Meeting with Bob',
                'description': 'Discuss project updates',
                'fallback_url': 'https://example.com/calendar-event',
            },
        ],
        'rcs': {
            'card_width': 'MEDIUM',
        },
        'channel': 'rcs',
        'message_type': 'carousel',
    }
    assert carousel.model_dump(by_alias=True, exclude_none=True) == carousel_dict


def test_create_rcs_carousel_without_rcs_options():
    with pytest.raises(ValidationError) as err:
        carousel = RcsCarousel(
            to='1234567890',
            from_='asdf1234',
            cards=[
                RcsCardItem(
                    title='Card title',
                    text='Card description',
                    media_url='https://example.com/image.jpg',
                    media_height='MEDIUM',
                )
            ] * 2,
        )
    assert "Field required" in str(err.value)


def test_create_rcs_carousel_with_insufficient_cards():
    with pytest.raises(ValidationError) as err:
        carousel = RcsCarousel(
            to='1234567890',
            from_='asdf1234',
            cards=[
                RcsCardItem(
                    title='Card title',
                    text='Card description',
                    media_url='https://example.com/image.jpg',
                    media_height='MEDIUM',
                )
            ],
            rcs=RcsOptionsCarousel(
                card_width='MEDIUM',
            ),
        )
    assert "List should have at least 2 items" in str(err.value)


def test_create_rcs_carousel_with_too_many_cards():
    with pytest.raises(ValidationError) as err:
        carousel = RcsCarousel(
            to='1234567890',
            from_='asdf1234',
            cards=[
                RcsCardItem(
                    title='Card title',
                    text='Card description',
                    media_url='https://example.com/image.jpg',
                    media_height='MEDIUM',
                )
            ]
            * 11,
            rcs=RcsOptionsCarousel(
                card_width='MEDIUM',
            ),
        )
    assert "List should have at most 10 items" in str(err.value)


def test_create_rcs_carousel_with_invalid_card_type():
    with pytest.raises(ValidationError) as err:
        carousel = RcsCarousel(
            to='1234567890',
            from_='asdf1234',
            cards=[
                RcsCardItem(
                    title='Card title',
                    text='Card description',
                    media_url='https://example.com/image.jpg',
                    media_height='MEDIUM',
                ),
                RcsCardMessage(
                    to='1234567890',
                    from_='asdf1234',
                    title='Card title',
                    text='Card description',
                    media_url='https://example.com/image.jpg',
                ),
            ],
            rcs=RcsOptionsCarousel(
                card_width='MEDIUM',
            ),
        )
    assert "Input should be a valid dictionary or instance" in str(err.value)


def test_create_rcs_carousel_with_insuffient_suggestions():
    with pytest.raises(ValidationError) as err:
        carousel = RcsCarousel(
            to='1234567890',
            from_='asdf1234',
            cards=[
                RcsCardItem(
                    title='Card title',
                    text='Card description',
                    media_url='https://example.com/image.jpg',
                    media_height='MEDIUM',
                )
            ]
            * 2,
            suggestions=[],
            rcs=RcsOptionsCarousel(
                card_width='MEDIUM',
            ),
        )
    assert "List should have at least 1 item" in str(err.value)


def test_create_rcs_carousel_with_too_many_suggestions():
    with pytest.raises(ValidationError) as err:
        carousel = RcsCarousel(
            to='1234567890',
            from_='asdf1234',
            cards=[
                RcsCardItem(
                    title='Card title',
                    text='Card description',
                    media_url='https://example.com/image.jpg',
                    media_height='MEDIUM',
                )
            ]
            * 2,
            suggestions=[
                RcsSuggestionReply(
                    text='Reply',
                    postback_data='postback-data',
                ),
            ]
            * 12,
            rcs=RcsOptionsCarousel(
                card_width='MEDIUM',
            ),
        )
    assert "List should have at most 11 items" in str(err.value)


def test_create_rcs_carousel_with_inavalid_suggestion_types():
    with pytest.raises(ValidationError) as err:
        carousel = RcsCarousel(
            to='1234567890',
            from_='asdf1234',
            cards=[
                RcsCardItem(
                    title='Card title',
                    text='Card description',
                    media_url='https://example.com/image.jpg',
                    media_height='MEDIUM',
                )
            ] * 2,
            suggestions=[
                RcsSuggestionReply(
                    text='Reply',
                    postback_data='postback-data',
                ),
                "Invalid suggestion type",
            ],
            rcs=RcsOptionsCarousel(
                card_width='MEDIUM',
            ),
        )
    assert "Input should be a valid dictionary or instance" in str(err.value)


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


def test_rcs_suggestion_base_without_text():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionBase(
            postback_data='postback-data',
        )
    assert "Field required" in str(err.value)


def test_rcs_suggestion_base_without_postback_data():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionBase(
            text='Reply',
        )
    assert "Field required" in str(err.value)


def test_rcs_suggestion_base_with_text_too_short():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionBase(
            text='',
            postback_data='postback-data',
        )
    assert "String should have at least 1 character" in str(err.value)


def test_rcs_suggestion_base_with_text_too_long():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionBase(
            text='A' * 25 + 'B',
            postback_data='postback-data',
        )
    assert "String should have at most 25 characters" in str(err.value)


def test_rcs_suggestion_reply():
    suggestion = RcsSuggestionReply(
        text='Reply',
        postback_data='postback-data',
    )
    suggestion_dict = {
        'type': 'reply',
        'text': 'Reply',
        'postback_data': 'postback-data',
    }

    assert suggestion.model_dump(by_alias=True, exclude_none=True) == suggestion_dict


def test_rcs_suggestion_dial():
    suggestion = RcsSuggestionActionDial(
        text='Call us',
        postback_data='postback-data',
        phone_number='447900000000',
    )
    suggestion_dict = {
        'type': 'dial',
        'text': 'Call us',
        'postback_data': 'postback-data',
        'phone_number': '447900000000',
    }

    assert suggestion.model_dump(by_alias=True, exclude_none=True) == suggestion_dict


def test_rcs_suggestion_action_dial_without_phone_number():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionDial(
            text='Call us',
            postback_data='postback-data',
        )
    assert "Field required" in str(err.value)


def test_rcs_suggestion_action_view_location():
    suggestion = RcsSuggestionActionViewLocation(
        text='View location',
        postback_data='postback-data',
        latitude='51.5074',
        longitude='-0.1278',
        pin_label='London',
        fallback_url='https://example.com/location',
    )
    suggestion_dict = {
        'type': 'view_location',
        'text': 'View location',
        'postback_data': 'postback-data',
        'latitude': '51.5074',
        'longitude': '-0.1278',
        'pin_label': 'London',
        'fallback_url': 'https://example.com/location',
    }
    assert suggestion.model_dump(by_alias=True, exclude_none=True) == suggestion_dict


def test_rcs_suggestion_action_view_location_without_latitude():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionViewLocation(
            text='View location',
            postback_data='postback-data',
            longitude='-0.1278',
            pin_label='London',
            fallback_url='https://example.com/location',
        )
    assert "Field required" in str(err.value)


def test_rcs_suggestion_action_view_location_without_longitude():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionViewLocation(
            text='View location',
            postback_data='postback-data',
            latitude='51.5074',
            pin_label='London',
            fallback_url='https://example.com/location',
        )
    assert "Field required" in str(err.value)


def test_rcs_suggestion_action_view_location_without_pin_label():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionViewLocation(
            text='View location',
            postback_data='postback-data',
            latitude='51.5074',
            longitude='-0.1278',
            fallback_url='https://example.com/location',
        )
    assert "Field required" in str(err.value)


def test_rcs_suggestion_action_share_location():
    suggestion = RcsSuggestionActionShareLocation(
        text='Share location',
        postback_data='postback-data',
    )
    suggestion_dict = {
        'type': 'share_location',
        'text': 'Share location',
        'postback_data': 'postback-data',
    }
    assert suggestion.model_dump(by_alias=True, exclude_none=True) == suggestion_dict


def test_rcs_suggestion_action_open_url():
    suggestion = RcsSuggestionActionOpenUrl(
        text='Open URL',
        postback_data='postback-data',
        url='https://example.com',
        description='Click to open the URL',
    )
    suggestion_dict = {
        'type': 'open_url',
        'text': 'Open URL',
        'postback_data': 'postback-data',
        'url': 'https://example.com',
        'description': 'Click to open the URL',
    }
    assert suggestion.model_dump(by_alias=True, exclude_none=True) == suggestion_dict


def test_rcs_suggestion_action_open_url_without_url():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionOpenUrl(
            text='Open URL',
            postback_data='postback-data',
            description='Click to open the URL',
        )
    assert "Field required" in str(err.value)


def test_rcs_suggestion_action_open_url_without_description():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionOpenUrl(
            text='Open URL',
            postback_data='postback-data',
            url='https://example.com',
        )
    assert "Field required" in str(err.value)


def test_rcs_suggestion_action_open_url_with_description_too_short():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionOpenUrl(
            text='Open URL',
            postback_data='postback-data',
            url='https://example.com',
            description='',
        )
    assert "String should have at least 1 character" in str(err.value)


def test_rcs_suggestion_action_open_url_with_description_too_long():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionOpenUrl(
            text='Open URL',
            postback_data='postback-data',
            url='https://example.com',
            description='A' * 500 + 'B',
        )
    assert "String should have at most 500 characters" in str(err.value)


def test_rcs_suggestion_action_open_url_in_webview():
    suggestion = RcsSuggestionActionOpenUrlWebview(
        text='Open URL',
        postback_data='postback-data',
        url='https://example.com',
        description='Click to open the URL',
        view_mode='FULL',
    )
    suggestion_dict = {
        'type': 'open_url_in_webview',
        'text': 'Open URL',
        'postback_data': 'postback-data',
        'url': 'https://example.com',
        'description': 'Click to open the URL',
        'view_mode': 'FULL',
    }
    assert suggestion.model_dump(by_alias=True, exclude_none=True) == suggestion_dict


def test_rcs_suggestion_action_open_url_in_webview_without_url():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionOpenUrlWebview(
            text='Open URL',
            postback_data='postback-data',
            description='Click to open the URL',
        )
    assert "Field required" in str(err.value)


def test_rcs_suggestion_action_open_url_in_webview_without_description():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionOpenUrlWebview(
            text='Open URL',
            postback_data='postback-data',
            url='https://example.com',
        )
    assert "Field required" in str(err.value)


def test_rcs_suggestion_action_open_url_in_webview_with_description_too_short():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionOpenUrlWebview(
            text='Open URL',
            postback_data='postback-data',
            url='https://example.com',
            description='',
        )
    assert "String should have at least 1 character" in str(err.value)


def test_rcs_suggestion_action_open_url_in_webview_with_description_too_long():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionOpenUrlWebview(
            text='Open URL',
            postback_data='postback-data',
            url='https://example.com',
            description='A' * 500 + 'B',
        )
    assert "String should have at most 500 characters" in str(err.value)


def test_rcs_suggestion_action_open_url_in_webview_with_invalid_view_mode():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionOpenUrlWebview(
            text='Open URL',
            postback_data='postback-data',
            url='https://example.com',
            description='Click to open the URL',
            view_mode='INVALID_VIEW_MODE',
        )
    assert "Input should be 'FULL', 'TALL' or 'HALF'" in str(err.value)


def test_rcs_suggestion_action_create_calendar_event():
    suggestion = RcsSuggestionActionCreateCalendarEvent(
        text='Add to calendar',
        postback_data='postback-data',
        start_time='2024-01-01T12:00:00Z',
        end_time='2024-01-01T13:00:00Z',
        title='Meeting with Bob',
        description='Discuss project updates',
        fallback_url='https://example.com/calendar-event',
    )
    suggestion_dict = {
        'type': 'create_calendar_event',
        'text': 'Add to calendar',
        'postback_data': 'postback-data',
        'start_time': '2024-01-01T12:00:00Z',
        'end_time': '2024-01-01T13:00:00Z',
        'title': 'Meeting with Bob',
        'description': 'Discuss project updates',
        'fallback_url': 'https://example.com/calendar-event',
    }
    assert suggestion.model_dump(by_alias=True, exclude_none=True) == suggestion_dict


def test_rcs_suggestion_action_create_calendar_event_without_start_time():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionCreateCalendarEvent(
            text='Add to calendar',
            postback_data='postback-data',
            end_time='2024-01-01T13:00:00Z',
            title='Meeting with Bob',
            description='Discuss project updates',
        )
    assert "Field required" in str(err.value)


def test_rcs_suggestion_action_create_calendar_event_without_end_time():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionCreateCalendarEvent(
            text='Add to calendar',
            postback_data='postback-data',
            start_time='2024-01-01T12:00:00Z',
            title='Meeting with Bob',
            description='Discuss project updates',
        )
    assert "Field required" in str(err.value)


def test_rcs_suggestion_action_create_calendar_event_without_title():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionCreateCalendarEvent(
            text='Add to calendar',
            postback_data='postback-data',
            start_time='2024-01-01T12:00:00Z',
            end_time='2024-01-01T13:00:00Z',
            description='Discuss project updates',
        )
    assert "Field required" in str(err.value)


def test_rcs_suggestion_action_create_calendar_event_without_description():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionCreateCalendarEvent(
            text='Add to calendar',
            postback_data='postback-data',
            start_time='2024-01-01T12:00:00Z',
            end_time='2024-01-01T13:00:00Z',
            title='Meeting with Bob',
        )
    assert "Field required" in str(err.value)


def test_rcs_suggestion_action_create_calendar_event_with_title_too_short():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionCreateCalendarEvent(
            text='Add to calendar',
            postback_data='postback-data',
            start_time='2024-01-01T12:00:00Z',
            end_time='2024-01-01T13:00:00Z',
            title='',
            description='Discuss project updates',
        )
    assert "String should have at least 1 character" in str(err.value)


def test_rcs_suggestion_action_create_calendar_event_with_title_too_long():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionCreateCalendarEvent(
            text='Add to calendar',
            postback_data='postback-data',
            start_time='2024-01-01T12:00:00Z',
            end_time='2024-01-01T13:00:00Z',
            title='A' * 100 + 'B',
            description='Discuss project updates',
        )
    assert "String should have at most 100 characters" in str(err.value)


def test_rcs_suggestion_action_create_calendar_event_with_description_too_short():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionCreateCalendarEvent(
            text='Add to calendar',
            postback_data='postback-data',
            start_time='2024-01-01T12:00:00Z',
            end_time='2024-01-01T13:00:00Z',
            title='Meeting with Bob',
            description='',
        )
    assert "String should have at least 1 character" in str(err.value)


def test_rcs_suggestion_action_create_calendar_event_with_description_too_long():
    with pytest.raises(ValidationError) as err:
        suggestion = RcsSuggestionActionCreateCalendarEvent(
            text='Add to calendar',
            postback_data='postback-data',
            start_time='2024-01-01T12:00:00Z',
            end_time='2024-01-01T13:00:00Z',
            title='Meeting with Bob',
            description='A' * 500 + 'B',
        )
    assert "String should have at most 500 characters" in str(err.value)


def test_create_rcs_options():
    options = RcsOptions(
        category='transaction',
    )
    options_dict = {
        'category': 'transaction',
    }
    assert options.model_dump(by_alias=True, exclude_none=True) == options_dict


def test_create_rcs_options_with_each_valid_category():
    valid_options = [
        'acknowledgement',
        'authentication',
        'promotion',
        'service-request',
        'transaction',
    ]
    for option in valid_options:
        options = RcsOptions(
            category=option,
        )
        options_dict = {
            'category': option,
        }
        assert options.model_dump(by_alias=True, exclude_none=True) == options_dict


def test_create_rcs_options_with_invalid_category():
    with pytest.raises(ValidationError) as err:
        options = RcsOptions(
            category='invalid-category',
        )
    assert (
        "Input should be 'acknowledgement', 'authentication', 'promotion', 'service-request' or 'transaction'"
        in str(err.value)
    )


def test_create_rcs_options_card():
    options = RcsOptionsCard(card_orientation='HORIZONTAL', image_alignment='LEFT')
    options_dict = {
        'card_orientation': 'HORIZONTAL',
        'image_alignment': 'LEFT',
    }
    assert options.model_dump(by_alias=True, exclude_none=True) == options_dict


def test_create_rcs_options_card_with_all_options():
    options = RcsOptionsCard(
        card_orientation='HORIZONTAL',
        image_alignment='LEFT',
        category='transaction',
    )
    options_dict = {
        'card_orientation': 'HORIZONTAL',
        'image_alignment': 'LEFT',
        'category': 'transaction',
    }
    assert options.model_dump(by_alias=True, exclude_none=True) == options_dict


def test_create_rcs_options_card_card_orientation_with_each_valid_option():
    valid_orientations = ['VERTICAL', 'HORIZONTAL']
    for orientation in valid_orientations:
        options = RcsOptionsCard(card_orientation=orientation, image_alignment='LEFT')
        options_dict = {
            'card_orientation': orientation,
            'image_alignment': 'LEFT',
        }
        assert options.model_dump(by_alias=True, exclude_none=True) == options_dict


def test_create_rcs_options_card_image_alignment_with_each_valid_option():
    valid_alignments = ['LEFT', 'RIGHT']
    for alignment in valid_alignments:
        options = RcsOptionsCard(card_orientation='HORIZONTAL', image_alignment=alignment)
        options_dict = {
            'card_orientation': 'HORIZONTAL',
            'image_alignment': alignment,
        }
        assert options.model_dump(by_alias=True, exclude_none=True) == options_dict


def test_create_rcs_options_card_card_orientation_with_invalid_option():
    with pytest.raises(ValidationError) as err:
        options = RcsOptionsCard(
            card_orientation='INVALID_ORIENTATION', image_alignment='LEFT'
        )
    assert "Input should be 'VERTICAL' or 'HORIZONTAL'" in str(err.value)


def test_create_rcs_options_card_image_alignment_with_invalid_option():
    with pytest.raises(ValidationError) as err:
        options = RcsOptionsCard(
            card_orientation='HORIZONTAL', image_alignment='INVALID_ALIGNMENT'
        )
    assert "Input should be 'LEFT' or 'RIGHT'" in str(err.value)


def test_create_rcs_options_carousel():
    options = RcsOptionsCarousel(
        card_width='MEDIUM',
    )
    options_dict = {
        'card_width': 'MEDIUM',
    }
    assert options.model_dump(by_alias=True, exclude_none=True) == options_dict


def test_create_rcs_options_carousel_with_all_options():
    options = RcsOptionsCarousel(
        card_width='MEDIUM',
        category='transaction',
    )
    options_dict = {
        'card_width': 'MEDIUM',
        'category': 'transaction',
    }
    assert options.model_dump(by_alias=True, exclude_none=True) == options_dict


def test_create_rcs_options_carousel_without_card_width():
    with pytest.raises(ValidationError) as err:
        options = RcsOptionsCarousel(
            category='transaction',
        )
    assert "Field required" in str(err.value)


def test_create_rcs_options_carousel_card_width_with_each_valid_option():
    valid_widths = ['SMALL', 'MEDIUM']
    for width in valid_widths:
        options = RcsOptionsCarousel(
            card_width=width,
        )
        options_dict = {
            'card_width': width,
        }
        assert options.model_dump(by_alias=True, exclude_none=True) == options_dict


def test_create_rcs_options_carousel_card_width_with_invalid_option():
    with pytest.raises(ValidationError) as err:
        options = RcsOptionsCarousel(
            card_width='INVALID_WIDTH',
        )
    assert "Input should be 'SMALL' or 'MEDIUM'" in str(err.value)
