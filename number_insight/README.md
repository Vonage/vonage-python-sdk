# Vonage Number Insight Package

This package contains the code to use [Vonage's Number Insight API](https://developer.vonage.com/en/number-insight/overview) in Python. This package includes methods to get information about phone numbers. It has 3 levels of insight: basic, standard, and advanced.

The advanced insight can be obtained synchronously or asynchronously. An async approach is recommended to avoid timeouts. Optionally, you can get caller name information (additional charge) by passing the `cnam` parameter to a standard or advanced insight request.

## Usage

It is recommended to use this as part of the main `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`.

### Make a Basic Number Insight Request
