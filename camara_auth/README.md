# Camara API Authentication Client

This package (`vonage-camara-auth`) provides a client for authenticating Camara APIs that require Oauth2 authentcation. Using it, it is possible to generate authenticated JWTs for use with GNP APIs, e.g. Sim Swap, Number Verification.

This package is not intended to be used directly, but will be called by Camara-based APIs that require it. Thus, it doesn't require manual installation or configuration unless you're using this package independently of an SDK.

For full API documentation, refer to the [Vonage developer documentation](https://developer.vonage.com).

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
