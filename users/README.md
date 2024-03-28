# Vonage Users Package

This package contains the code to use Vonage's Users API in Python.

It includes methods for managing users.

## Usage

It is recommended to use this as part of the main `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`.

### List Users

With no custom options specified, this method will get the last 100 users. It returns a tuple consisting of a list of `UserSummary` objects and a string describing the cursor to the next page of results.

```python
from vonage_users import ListUsersRequest

users, _ = vonage_client.users.list_users()

# With options
params = ListUsersRequest(
    page_size=10,
    cursor=my_cursor,
    order='desc',
)
users, next_cursor = vonage_client.users.list_users(params)
```

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