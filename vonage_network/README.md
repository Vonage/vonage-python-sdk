# Vonage Network API Python SDK

The Vonage Network API Python SDK Package `vonage-network` provides a streamlined interface for using Vonage APIs in Python projects. This package includes the `VonageNetwork` class, which simplifies API interactions.

The `VonageNetwork` class in this package serves as an entry point for using [Vonage Network APIs](https://developer.vonage.com/en/getting-started-network/what-are-network-apis). It abstracts away complexities with authentication, HTTP requests and more.

For full API documentation refer to the [Vonage Developer documentation](https://developer.vonage.com).

Please note this package is in beta and could be subject to change or removal.

## Installation

Install the package using pip:

```bash
pip install vonage-network
```

## Usage

```python
from vonage_network import VonageNetwork, Auth, HttpClientOptions

# Create an Auth instance
auth = Auth(api_key='your_api_key', api_secret='your_api_secret')

# Create HttpClientOptions instance
# (not required unless you want to change options from the defaults)
options = HttpClientOptions(api_host='api.nexmo.com', timeout=30)

# Create a Vonage network client instance
vonage_network = VonageNetwork(auth=auth, http_client_options=options)
```

The `VonageNetwork` class provides access to various Vonage Network APIs through its properties. For example, to call the Network Sim Swap API:

```python
from vonage_network_sim_swap import SwapStatus
swap_status: SwapStatus = vonage_network.sim_swap.check(phone_number='MY_NUMBER')
print(swap_status.swapped)
```

You can also access the underlying `HttpClient` instance through the `http_client` property:

```python
user_agent = vonage_network.http_client.user_agent
```