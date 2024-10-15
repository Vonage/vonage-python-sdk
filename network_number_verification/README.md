# Vonage Number Verification Network API Client

This package (`vonage-network-number-verification`) allows you to verify a mobile device. It verifies the phone number linked to the SIM card in a device which is connected to a mobile data network, without any user input.

This package is not intended to be used directly, instead being accessed from an enclosing SDK package. Thus, it doesn't require manual installation or configuration unless you're using this package independently of an SDK.

For full API documentation, refer to the [Vonage developer documentation](https://developer.vonage.com).

Please note this package is in beta.

## Registering to Use the Network Number Verification API

To use this API, you must first create and register a business profile with the Vonage Network Registry. [This documentation page](https://developer.vonage.com/en/getting-started-network/registration) explains how this can be done. You need to obtain approval for each network and region you want to use the APIs in.

## Installation

Install from the Python Package Index with pip:

```bash
pip install vonage-network-number-verifcation
```

## Usage

It is recommended to use this as part of the `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`.

The Vonage Number Verification API uses Oauth2 authentication, which this SDK will also help you to do. Verifying a number has 3 stages:

1. Get an OIDC URL for use in your front-end application
2. Create an Access Token from an Authentication Code
3. Make a Number Verification Request

### Get an OIDC URL

```python
```

### Create an Access Token

```python
```

### Make a Number Verification Request

```python
```