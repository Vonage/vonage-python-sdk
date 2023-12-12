# Migration guide from OpenTok Python SDK to Vonage Python SDK

## Installation

You can now interact with Vonage's Video API using the `vonage` PyPI package rather than the `opentok` PyPI package. To do this, create a virtual environment and install the `vonage` package in your virtual environment using this command:

```bash
python3 -m venv venv-vonage-video
. ./venv-vonage-video/bin/activate
pip install vonage
```

Note: not all the Video API features are yet supported in the `vonage` package. There is a full list of [Supported Features](#supported-features) later in this document.

## Setup

Whereas the `opentok` package used an `api_key` and `api_secret` for Authorization, the Video API implementation in the `vonage` package uses a JWT. The SDK handles JWT generation in the background for you, but will require an `application_id` and `private_key` as credentials in order to generate the token. You can obtain these by setting up a Vonage Application, which you can create via the [Developer Dashboard](https://dashboard.nexmo.com/applications). (The Vonage Application is also where you can set other settings such as callback URLs, storage preferences, etc).

These credentials are then passed in when instantiating a `Client` object (the example below assumes you have these set as environment variables):

```python
import vonage

client = vonage.Client(
	application_id='VONAGE_APPLICATION_ID',
	private_key='VONAGE_PRIVATE_KEY_PATH',
)
```

You can access the Video API via the `Video` class stored at `Client.video`. To call methods related to the Video API, use this syntax:

```python
client.video.video_api_method...
```

You can interact with the Vonage Video API via various methods, for example:

- Create a Session

```python
# Pass options for the session as a Python dictionary in SESSION_OPTIONS
session = client.video.create_session(SESSION_OPTIONS)
```

- Retrieve a List of Archive Recordings

```python
archive_list = client.video.list_archives(FILTER_OPTIONS)
```

## Changed Methods

There are some changes to methods between the `opentok` SDK and the Video API implementation in the `vonage` SDK.

- Any positional parameters in method signatures have been replaced with keyword parameters in the `vonage` package.
- Methods now return the response as a Python dictionary.
- Some methods have been renamed, for clarity and/or to better reflect what the method does. These are listed below:

| OpenTok Method Name | Vonage Video Method Name |
|---|---|
| `opentok.generate_token` | `video.generate_client_token` |
| `opentok.start_archive` | `video.create_archive` |
| `opentok.add_archive_stream` | `video.add_stream_to_archive` |
| `opentok.remove_archive_stream` | `video.remove_stream_from_archive` |
| `opentok.set_archive_layout` | `video.change_archive_layout` |
| `opentok.add_broadcast_stream` | `video.add_stream_to_broadcast` |
| `opentok.remove_broadcast_stream` | `video.remove_stream_from_broadcast` |
| `opentok.set_broadcast_layout` | `video.change_broadcast_layout` |
| `opentok.set_stream_class_lists` | `video.set_stream_layout` |
| `opentok.force_disconnect` | `video.disconnect_client` |
| `opentok.mute_all` | `video.mute_all_streams` |
| `opentok.disable_force_mute` | `video.disable_mute_all_streams`|
| `opentok.dial` | `video.create_sip_call`|

## Supported Features

The following is a list of Vonage Video APIs and whether the SDK provides support for them:

| API   |  Supported?
|----------|:-------------:|
| Session Creation | ✅ |
| Stream Management | ✅ |
| Signaling | ✅ |
| Moderation | ✅ |
| Archiving | ✅ |
| Live Streaming Broadcasts | ✅ |
| SIP Interconnect | ✅ |
| Account Management | ❌ |
| Experience Composer | ❌ |
| Audio Connector | ❌ |
| Live Captions | ❌ |
| Custom S3/Azure buckets | ❌ |