# Vonage HTTP Client Package

This Python package provides a synchronous HTTP client for sending authenticated requests to Vonage APIs.

This package (`vonage-http-client`) is used by the `vonage` Python package and SDK so doesn't require manual installation or config unless you're using this package independently of a SDK.

The `HttpClient` class is initialized with an instance of the `Auth` class for credentials, an optional class of HTTP client options, and an optional SDK version (this is provided automatically when using this module via an SDK).

The `HttpClientOptions` class defines the options for the HTTP client, including the API and REST hosts, timeout, pool connections, pool max size, and max retries.

This package also includes an `Auth` class that allows you to manage API key- and secret-based authentication as well as JSON Web Token (JWT) authentication.

For full API documentation refer to the [Vonage Developer documentation](https://developer.vonage.com).

## Installation (if not using via an SDK)

You can install the package using pip:

```bash
pip install vonage-http-client
```

## Usage

```python
from vonage_http_client import HttpClient, HttpClientOptions
from vonage_http_client.auth import Auth

# Create an Auth instance
auth = Auth(api_key='your_api_key', api_secret='your_api_secret')

# Create HttpClientOptions instance
options = HttpClientOptions(api_host='api.nexmo.com', timeout=30)

# Create a HttpClient instance
client = HttpClient(auth=auth, http_client_options=options)

# Make a GET request
response = client.get(host='api.nexmo.com', request_path='/v1/messages')

# Make a POST request
response = client.post(host='api.nexmo.com', request_path='/v1/messages', params={'key': 'value'})
```

## Get the Last Request and Last Response from the HTTP Client

The `HttpClient` class exposes two properties, `last_request` and `last_response` that cache the last sent request and response.

```python
# Get last request, has type requests.PreparedRequest
request = client.last_request

# Get last response, has type requests.Response
response = client.last_response
```

### Appending to the User-Agent Header

The `HttpClient` class also supports appending additional information to the User-Agent header via the append_to_user_agent method:

```python
client.append_to_user_agent('additional_info')
```

### Changing the Authentication Method Used

The `HttpClient` class automatically handles JWT and basic authentication based on the Auth instance provided. It uses JWT authentication by default, but you can specify the authentication type when making a request:

```python
# Use basic authentication for this request
response = client.get(host='api.nexmo.com', request_path='/v1/messages', auth_type='basic')
```

### Catching errors

Error objects are exposed in the package scope, so you can catch errors like this:

```python
from vonage_http_client import HttpRequestError

try:
    client.post(...)
except HttpRequestError:
    ...
```