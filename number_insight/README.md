# Vonage Number Insight Package

This package contains the code to use [Vonage's Number Insight API](https://developer.vonage.com/en/number-insight/overview) in Python. This package includes methods to get information about phone numbers. It has 3 levels of insight: basic, standard, and advanced.

The advanced insight can be obtained synchronously or asynchronously. An async approach is recommended to avoid timeouts. Optionally, you can get caller name information (additional charge) by passing the `cnam` parameter to a standard or advanced insight request.

## Usage

It is recommended to use this as part of the main `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`.

### Make a Basic Number Insight Request

```python
from vonage_number_insight import BasicInsightRequest

response = vonage_client.number_insight.basic_number_insight(
    BasicInsightRequest(number='12345678900')
)

print(response.model_dump(exclude_none=True))
```

### Make a Standard Number Insight Request

```python
from vonage_number_insight import StandardInsightRequest

vonage_client.number_insight.standard_number_insight(
    StandardInsightRequest(number='12345678900')
)

# Optionally, you can get caller name information (additional charge) by setting the `cnam` parameter = True
vonage_client.number_insight.standard_number_insight(
    StandardInsightRequest(number='12345678900', cnam=True)
)
```

### Make an Asynchronous Advanced Number Insight Request

When making an asynchronous advanced number insight request, the API will return basic information about the request to you immediately and send the full data to the webhook callback URL you specify.

```python
from vonage_number_insight import AdvancedAsyncInsightRequest

vonage_client.number_insight.advanced_async_number_insight(
    AdvancedAsyncInsightRequest(callback='https://example.com', number='12345678900')
)
```

### Make a Synchronous Advanced Number Insight Request

```python
from vonage_number_insight import AdvancedSyncInsightRequest

vonage_client.number_insight.advanced_sync_number_insight(
    AdvancedSyncInsightRequest(number='12345678900')
)
```