# Vonage Number Verification Network API Client

This package (`vonage-network-number-verification`) allows you to verify a mobile device. It verifies the phone number linked to the SIM card in a device which is connected to a mobile data network, without any user input.

This package is not intended to be used directly, instead being accessed from an enclosing SDK package. Thus, it doesn't require manual installation or configuration unless you're using this package independently of an SDK.

For full API documentation, refer to the [Vonage developer documentation](https://developer.vonage.com).

## Registering to Use the Network Number Verification API

To use this API, you must first create and register a business profile with the Vonage Network Registry. [This documentation page](https://developer.vonage.com/en/getting-started-network/registration) explains how this can be done. You need to obtain approval for each network and region you want to use the APIs in.

## Installation

Install from the Python Package Index with pip:

```bash
pip install vonage-network-number-verification
```

## Usage

It is recommended to use this as part of the `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`.

The Vonage Number Verification API uses Oauth2 authentication, which this SDK will also help you to do. Verifying a number has 3 stages:

1. Get an OIDC URL for use in your front-end application
2. Use this URL in your own application to get an authorization code
3. Make a Number Verification Request using this code to verify the number

This package contains methods to help with Steps 1 and 3.

### Get an OIDC URL

```python
from vonage_network_number_verification import CreateOidcUrl

url_options = CreateOidcUrl(
    redirect_uri='https://example.com/redirect',
    state='c9896ee6-4ff8-464c-b393-d56d6e638f88',
    login_hint='+990123456',
)

url = number_verification.get_oidc_url(url_options)
print(url)
```

Get your user's device to follow this URL and a code to use for number verification will be returned in the final redirect query parameters. Note: your user must be connected to their mobile network.

### Make a Number Verification Request

```python
from vonage_network_number_verification import NumberVerificationRequest

response = number_verification.verify(
    NumberVerificationRequest(
        code='code',
        redirect_uri='https://example.com/redirect',
        phone_number='+990123456',
    )
)
print(response.device_phone_number_verified)
```