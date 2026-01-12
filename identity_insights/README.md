# Vonage Identity Insights Package

This package contains the code to use the [Vonage Identity Insights API](https://developer.vonage.com/en/identity-insights/overview) in Python. The API provides real-time access to a broad range of attributes related to the carrier, subscriber, or device associated with a phone number. To use it you will need a Vonage account. Sign up [for free at vonage.com][signup].

## Usage

It is recommended to use this as part of the main `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`.

### Make a Standard Identity Insights Request

```python
from vonage import Vonage, Auth, HttpClientOptions
from vonage_identity_insights import (
    IdentityInsightsRequest,
    InsightsRequest,
    EmptyInsight,
    SimSwapInsight,
)

options = HttpClientOptions(api_host="api-eu.vonage.com", timeout=30)

client = Vonage(auth=auth, http_client_options=options)

request = IdentityInsightsRequest(
    phone_number="1234567890",
    purpose="FraudPreventionAndDetection",
    insights=InsightsRequest(
        format=EmptyInsight(), sim_swap=SimSwapInsight(period=240)
    ),
)

response = client.identity_insights.requests(request)

```

