# Vonage Sim Swap Network API Client

This package (`vonage-network-sim-swap`) allows you to check whether a SIM card has been swapped, and the last swap date.

This package is not intended to be used directly, instead being accessed from an enclosing SDK package. Thus, it doesn't require manual installation or configuration unless you're using this package independently of an SDK.

For full API documentation, refer to the [Vonage developer documentation](https://developer.vonage.com).

## Registering to Use the Sim Swap API

To use this API, you must first create and register your business profile with the Vonage Network Registry. [This documentation page](https://developer.vonage.com/en/getting-started-network/registration) explains how this can be done. You need to obtain approval for each network and region you want to use the APIs in.

## Installation

Install from the Python Package Index with pip:

```bash
pip install vonage-camara-auth
```

## Usage

### Create a `CamaraAuth` Object

```python
from vonage_camara_auth import CamaraAuth
from vonage_http_client import HttpClient, Auth

camara_auth = CamaraAuth(HttpClient(Auth(application_id='application-id', private_key='private-key')))
```

### Generate an Authenticated Access Token

```python
token = camara_auth.get_oauth2_user_token(
    number='447700900000', scope='dpv:FraudPreventionAndDetection#check-sim-swap'
)
```
