import pytest
from pydantic import ValidationError
from vonage_messages.models import (
    EmailText,
    EmailHtml,
    EmailContent,
    EmailHtmlItem,
    EmailOptions,
    EmailAdditionalRecipient,
)
from vonage_messages.models.enums import WebhookVersion, EmailImportance, EmailPriority, EmailSensitivity

def test_create_email_additional_recipient():
    additional_recipient = EmailAdditionalRecipient(
        address='john.doe@example.com',
        name='John Doe'
    )
    additional_recipient_dict = {
        'address': 'john.doe@example.com',
        'name': 'John Doe'
    }

    assert additional_recipient.model_dump(exclude_none=True) == additional_recipient_dict


def test_create_email_additional_recipient_without_address():
    with pytest.raises(ValidationError) as err:
        additional_recipient = EmailAdditionalRecipient(
            name='John Doe'
        )

    assert "Field required" in str(err.value)


def test_create_email_options():
    email_options = EmailOptions(
        subject='Hello',
    )
    email_options_dict = {
        'subject': 'Hello',
    }

    assert email_options.model_dump(exclude_none=True) == email_options_dict


def test_create_email_options_all_fields():
    email_options = EmailOptions(
        subject='Hello',
        to_name='John Doe',
        from_name='Jane Doe',
        importance=EmailImportance.HIGH,
        priority=EmailPriority.NORMAL,
        sensitivity=EmailSensitivity.PRIVATE,
        cc=[EmailAdditionalRecipient(
            address='john.doe@example.com',
            name='John Doe'
        )],
        bcc=[EmailAdditionalRecipient(
            address='jane.doe@example.com',
            name='Jane Doe'
        )],
        reply_to='no-reply@my-domain.com',
    )
    email_options_dict = {
        'subject': 'Hello',
        'to_name': 'John Doe',
        'from_name': 'Jane Doe',
        'importance': 'high',
        'priority': 'normal',
        'sensitivity': 'private',
        'cc': [
            {
                'address': 'john.doe@example.com',
                'name': 'John Doe'
            }
        ],
        'bcc': [
            {
                'address': 'jane.doe@example.com',
                'name': 'Jane Doe'
            }
        ],
        'reply_to': 'no-reply@my-domain.com',
    }

    assert email_options.model_dump(exclude_none=True) == email_options_dict


def test_create_email_options_without_subject():
    with pytest.raises(ValidationError) as err:
        email_options = EmailOptions(
            to_name='John Doe',
            from_name='Jane Doe',
        )

    assert "Field required" in str(err.value)


def test_create_email_text():
    email_text_model = EmailText(
        to='john.doe@example.com',
        from_='no-reply@my-domain.com',
        text='Hello, world!',
        email=EmailOptions(
            subject='Hello'
        ),
    )
    email_text_dict = {
        'to': 'john.doe@example.com',
        'from': 'no-reply@my-domain.com',
        'text': 'Hello, world!',
        'channel': 'email',
        'message_type': 'text',
        'email': {
            'subject': 'Hello'
        },
    }

    assert email_text_model.model_dump(by_alias=True, exclude_none=True) == email_text_dict


def test_create_email_text_all_fields():
    email_text_model = EmailText(
        to='john.doe@example.com',
        from_='no-reply@my-domain.com',
        text='Hello, world!',
        email=EmailOptions(
            subject='Hello'
        ),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
    )
    email_text_dict = {
        'to': 'john.doe@example.com',
        'from': 'no-reply@my-domain.com',
        'text': 'Hello, world!',
        'channel': 'email',
        'message_type': 'text',
        'email': {
            'subject': 'Hello'
        },
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1'
    }

    assert email_text_model.model_dump(by_alias=True, exclude_none=True) == email_text_dict


def test_create_email_html_item():
    email_html_item = EmailHtmlItem(
        body='<p>Hello, world!</p>',
    )
    email_html_item_dict = {
        'body': '<p>Hello, world!</p>',
    }

    assert email_html_item.model_dump(exclude_none=True) == email_html_item_dict


def test_create_email_html_item_without_body():
    with pytest.raises(ValidationError) as err:
        email_html_item = EmailHtmlItem()

    assert "Field required" in str(err.value)


def test_create_email_html():
    email_html_model = EmailHtml(
        to='john.doe@example.com',
        from_='no-reply@my-domain.com',
        html=EmailHtmlItem(
            body='<p>Hello, world!</p>',
        ),
        email=EmailOptions(
            subject='Hello'
        ),
    )
    email_html_dict = {
        'to': 'john.doe@example.com',
        'from': 'no-reply@my-domain.com',
        'html': {
            'body': '<p>Hello, world!</p>'
        },
        'channel': 'email',
        'message_type': 'html',
        'email': {
            'subject': 'Hello'
        },
    }

    assert email_html_model.model_dump(by_alias=True, exclude_none=True) == email_html_dict


def test_create_email_html_all_fields():
    email_html_model = EmailHtml(
        to='john.doe@example.com',
        from_='no-reply@my-domain.com',
        html=EmailHtmlItem(
            body='<p>Hello, world!</p>',
        ),
        email=EmailOptions(
            subject='Hello'
        ),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
    )
    email_html_dict = {
        'to': 'john.doe@example.com',
        'from': 'no-reply@my-domain.com',
        'html': {
            'body': '<p>Hello, world!</p>'
        },
        'channel': 'email',
        'message_type': 'html',
        'email': {
            'subject': 'Hello'
        },
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1'
    }

    assert email_html_model.model_dump(by_alias=True, exclude_none=True) == email_html_dict


def test_create_email_content_element_text():
    email_content_element = EmailContentElementText(
        type='text',
        text='Hello, world!',
    )
    email_content_element_dict = {
        'type': 'text',
        'text': 'Hello, world!',
    }

    assert email_content_element.model_dump(exclude_none=True) == email_content_element_dict


def test_create_email_content_element_text_without_type():
    with pytest.raises(ValidationError) as err:
        email_content_element = EmailContentElementText(
            text='Hello, world!',
        )

    assert "Field required" in str(err.value)


def test_create_email_content_element_text_without_text():
    with pytest.raises(ValidationError) as err:
        email_content_element = EmailContentElementText(
            type='text',
        )

    assert "Field required" in str(err.value)


def test_create_email_content_element_html():
    email_content_element = EmailContentElementHtml(
        type='html',
        body='<p>Hello, world!</p>',
    )
    email_content_element_dict = {
        'type': 'html',
        'body': '<p>Hello, world!</p>',
    }

    assert email_content_element.model_dump(exclude_none=True) == email_content_element_dict


def test_create_email_content_element_html_without_type():
    with pytest.raises(ValidationError) as err:
        email_content_element = EmailContentElementHtml(
            body='<p>Hello, world!</p>',
        )

    assert "Field required" in str(err.value)


def test_create_email_content_element_html_without_body():
    with pytest.raises(ValidationError) as err:
        email_content_element = EmailContentElementHtml(
            type='html',
        )

    assert "Field required" in str(err.value)


def test_create_email_content():
    email_content_model = EmailContent(
        to='john.doe@example.com',
        from_='no-reply@my-domain.com',
        content=[
            EmailContentElementText(
                type='text',
                text='Hello, world!'
            )
        ],
        email=EmailOptions(
            subject='Hello'
        ),
    )
    email_content_dict = {
        'to': 'john.doe@example.com',
        'from': 'no-reply@my-domain.com',
        'content': [
            {
                'type': 'text',
                'text': 'Hello, world!'
            }
        ],
        'channel': 'email',
        'message_type': 'html',
        'email': {
            'subject': 'Hello'
        },
    }

    assert email_content_model.model_dump(by_alias=True, exclude_none=True) == email_content_dict


def test_create_email_content_all_fields():
    email_content_model = EmailContent(
        to='john.doe@example.com',
        from_='no-reply@my-domain.com',
        content=[
            EmailContentElementText(
                type='text',
                text='Hello, world!'
            )
        ],
        email=EmailOptions(
            subject='Hello'
        ),
        client_ref='client-ref',
        webhook_url='https://example.com',
        webhook_version=WebhookVersion.V1,
    )
    email_content_dict = {
        'to': 'john.doe@example.com',
        'from': 'no-reply@my-domain.com',
        'content': [
            {
                'type': 'text',
                'text': 'Hello, world!'
            }
        ],
        'channel': 'email',
        'message_type': 'html',
        'email': {
            'subject': 'Hello'
        },
        'client_ref': 'client-ref',
        'webhook_url': 'https://example.com',
        'webhook_version': 'v1',
    }

    assert email_content_model.model_dump(by_alias=True, exclude_none=True) == email_content_dict


def test_create_email_content_all_content_types():
    email_content_model = EmailContent(
        to='john.doe@example.com',
        from_='no-reply@my-domain.com',
        content=[
            EmailContentElementText(
                type='text',
                text='Hello, world!'
            ),
            EmailContentElementHtml(
                type='html',
                html='<p>Hello, world!</p>'
            )
        ],
        email=EmailOptions(
            subject='Hello'
        ),
    )
    email_content_dict = {
        'to': 'john.doe@example.com',
        'from': 'no-reply@my-domain.com',
        'content': [
            {
                'type': 'text',
                'text': 'Hello, world!'
            },
            {
                'type': 'html',
                'html': '<p>Hello, world!</p>'
            }
        ],
        'channel': 'email',
        'message_type': 'html',
        'email': {
            'subject': 'Hello'
        },
    }

    assert email_content_model.model_dump(by_alias=True, exclude_none=True) == email_content_dict


def test_create_email_content_with_invalid_content_item():
    with pytest.raises(ValidationError) as err:
        email_content_model = EmailContent(
            to='john.doe@example.com',
            from_='no-reply@my-domain.com',
            content=[
                EmailHtmlItem(
                    body='<p>Hello, world!</p>',
                )
            ],
            email=EmailOptions(
                subject='Hello'
            ),
        )

    assert "Input should be a valid dictionary or instance" in str(err.value)
