# Vonage Users Package

This package contains the code to use Vonage's Users API in Python.

It includes methods for managing users.

## Usage

It is recommended to use this as part of the main `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`.

### List Users

### Create a New User

### Get a User

### Update a User

### Delete a User

<!-- ### Manage a User

Create a `User` object, then pass into the `Users.create` or `Users.update` method.

```python
from vonage_users import User, UserResponse

user = User(name='John Doe', email='john.doe@example.com')
response: UserResponse = vonage_client.users.create(user)

print(response.model_dump(exclude_unset=True)) -->
