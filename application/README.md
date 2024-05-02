# Vonage Users Package

This package contains the code to use Vonage's Application API in Python.

It includes methods for managing applications.

## Usage

It is recommended to use this as part of the main `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`.

### List Applications

With no custom options specified, this method will get the first 100 applications. It returns a tuple consisting of a list of `ApplicationData` objects and an int showing the page number of the next page of results.

```python
from vonage_application import ListApplicationsFilter, ApplicationData

applications, next_page = vonage_client.application.list_applications()

# With options
options = ListApplicationsFilter(page_size=3, page=2)
applications, next_page = vonage_client.applications.list_applications(options)
```


--------


### Create a New User

```python
from vonage_users import User, Channels, SmsChannel
user_options = User(
    name='my_user_name',
    display_name='My User Name',
    properties={'custom_key': 'custom_value'},
    channels=Channels(sms=[SmsChannel(number='1234567890')]),
)
user = vonage_client.users.create_user(user_options)
```

### Get a User

```python
user = client.users.get_user('USR-87e3e6b0-cd7b-45ef-a0a7-bcd5566a672b')
user_as_dict = user.model_dump(exclude_none=True)
```

### Update a User
```python
from vonage_users import User, Channels, SmsChannel, WhatsappChannel
user_options = User(
    name='my_user_name',
    display_name='My User Name',
    properties={'custom_key': 'custom_value'},
    channels=Channels(sms=[SmsChannel(number='1234567890')], whatsapp=[WhatsappChannel(number='9876543210')]),
)
user = vonage_client.users.update_user(id, user_options)
```

### Delete a User

```python
vonage_client.users.delete_user(id)
```