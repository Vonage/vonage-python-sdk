# Vonage Network API Authentication Client

This package (`vonage-network-auth`) provides a client for authenticating Network APIs that require Oauth2 authentcation. Using it, it is possible to generate authenticated JWTs for use with GNP APIs, e.g. Sim Swap, Number Verification.

This package is intended to be used as part of an SDK, accessing required methods through the SDK instead of directly. Thus, it doesn't require manual installation or configuration unless you're using this package independently of an SDK.

For full API documentation, refer to the [Vonage developer documentation](https://developer.vonage.com).

Please note this package is in beta.

## Installation

Install from the Python Package Index with pip:

```bash
pip install vonage-network-auth
```

## Usage

### Create a `NetworkAuth` Object

```python
from vonage_network_auth import NetworkAuth
from vonage_http_client import HttpClient, Auth

network_auth = NetworkAuth(HttpClient(Auth(application_id='application-id', private_key='private-key')))
```

### Generate an Authenticated Access Token

```python
token = network_auth.get_oauth2_user_token(
    number='447700900000', scope='dpv:FraudPreventionAndDetection#check-sim-swap'
)
```
