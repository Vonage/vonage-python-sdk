# Vonage Sim Swap Network API Client

This package (`vonage-network-sim-swap`) allows you to check whether a SIM card has been swapped, and the last swap date.

This package is not intended to be used directly, instead being accessed from an enclosing SDK package. Thus, it doesn't require manual installation or configuration unless you're using this package independently of an SDK.

For full API documentation, refer to the [Vonage developer documentation](https://developer.vonage.com).

Please note this package is in beta.

## Registering to Use the Sim Swap API

To use this API, you must first create and register your business profile with the Vonage Network Registry. [This documentation page](https://developer.vonage.com/en/getting-started-network/registration) explains how this can be done. You need to obtain approval for each network and region you want to use the APIs in.

## Installation

Install from the Python Package Index with pip:

```bash
pip install vonage-network-sim-swap
```

## Usage

It is recommended to use this as part of the `vonage-network` package. The examples below assume you've created an instance of the `vonage_network.VonageNetwork` class called `network_client`.

### Check if a SIM Has Been Swapped

```python
from vonage_network_sim_swap import SwapStatus
swap_status: SwapStatus = vonage_network.sim_swap.check(phone_number='MY_NUMBER')
print(swap_status.swapped)
```

### Get the Date of the Last SIM Swap

```python
from vonage_network_sim_swap import LastSwapDate
swap_date: LastSwapDate = vonage_network.sim_swap.get_last_swap_date
print(swap_date.last_swap_date)
```