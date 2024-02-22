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

The Vonage class provides access to various Vonage APIs through its properties. For example, to use methods to call the Number Insight API v2:

```python
from vonage_number_insight_v2 import FraudCheckRequest

vonage.number_insight_v2.fraud_check(FraudCheckRequest(phone='1234567890'))
```

You can also access the underlying `HttpClient` instance through the `http_client` property:

```python
user_agent = vonage.http_client.user_agent
```