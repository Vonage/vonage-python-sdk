# Vonage Voice Package

This package contains the code to use [Vonage's Voice API](https://developer.vonage.com/en/voice/voice-api/overview) in Python. This package includes methods for working with the Voice API. It also contains an NCCO (Call Control Object) builder to help you to control call flow.

## Usage

It is recommended to use this as part of the main `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`.

### Create a Call


### Note on URLs

The Voice API requires most URLs to be passed in a list with only one element. When creating models, simply pass the url and the model will marshal it into the correct structure for you.

e.g.

```python
# Don't do this


# Do this

```