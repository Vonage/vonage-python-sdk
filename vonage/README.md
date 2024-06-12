# Vonage Python SDK

The Vonage Python SDK Package `vonage` provides a streamlined interface for using Vonage APIs in Python projects. This package includes the `Vonage` class, which simplifies API interactions.

The Vonage class in this package serves as the main entry point for using Vonage APIs. It abstracts away complexities with authentication, HTTP requests and more.

For full API documentation refer to the [Vonage Developer documentation](https://developer.vonage.com).

## Installation

Install the package using pip:

```bash
pip install vonage
```

## Usage

```python
from vonage import Vonage, Auth, HttpClientOptions

# Create an Auth instance
auth = Auth(api_key='your_api_key', api_secret='your_api_secret')

# Create HttpClientOptions instance
# (not required unless you want to change options from the defaults)
options = HttpClientOptions(api_host='api.nexmo.com', timeout=30)

# Create a Vonage instance
vonage = Vonage(auth=auth, http_client_options=options)
```

The Vonage class provides access to various Vonage APIs through its properties. For example, to use methods to call the SMS API:

```python
from vonage_sms import SmsMessage

message = SmsMessage(to='1234567890', from_='Vonage', text='Hello World')
response = client.sms.send(message)
print(response.model_dump_json(exclude_unset=True))
```

You can also access the underlying `HttpClient` instance through the `http_client` property:

```python
user_agent = vonage.http_client.user_agent
```