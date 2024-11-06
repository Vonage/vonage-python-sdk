# Vonage Application API Package

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
applications, next_page = vonage_client.application.list_applications(options)
```

### Create a New Application

```python
from vonage_application import ApplicationConfig

app_data = vonage_client.application.create_application()

# Create with custom options (can also be done with a dict)
from vonage_application import ApplicationConfig, Keys, Voice, VoiceWebhooks
voice = Voice(
    webhooks=VoiceWebhooks(
        event_url=VoiceUrl(
            address='https://example.com/event',
            http_method='POST',
            connect_timeout=500,
            socket_timeout=3000,
        ),
    ),
    signed_callbacks=True,
)
capabilities = Capabilities(voice=voice)
keys = Keys(public_key='MY_PUBLIC_KEY')
config = ApplicationConfig(
    name='My Customised Application',
    capabilities=capabilities,
    keys=keys,
)
app_data = vonage_client.application.create_application(config)
```

### Get an Application

```python
app_data = client.application.get_application('MY_APP_ID')
app_data_as_dict = app.model_dump(exclude_none=True)
```

### Update an Application

To update an application, pass config for the updated field(s) in an ApplicationConfig object

```python
from vonage_application import ApplicationConfig, Keys, Voice, VoiceWebhooks

config = ApplicationConfig(name='My Updated Application')
app_data = vonage_client.application.update_application('MY_APP_ID', config)
```

### Delete an Application

```python
vonage_client.applications.delete_application('MY_APP_ID')
```