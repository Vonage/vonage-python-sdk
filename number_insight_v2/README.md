# Vonage Number Insight Python SDK package

This package contains the code to use v2 of Vonage's Number Insight API (currently in beta) in Python.

It includes classes for making fraud check requests and handling the responses.

## Usage
First, import the necessary classes and create an instance of the `NumberInsightV2` class:

```python
from vonage_http_client.http_client import HttpClient
from number_insight_v2 import NumberInsightV2, FraudCheckRequest

http_client = HttpClient(api_host='your_api_host', api_key='your_api_key', api_secret='your_api_secret')
number_insight = NumberInsightV2(http_client)
```

You can then create a `FraudCheckRequest` object and use the `fraud_check` method to initiate a fraud check request:

```python
request = FraudCheckRequest(phone='1234567890')
response = number_insight.fraud_check(request)
```