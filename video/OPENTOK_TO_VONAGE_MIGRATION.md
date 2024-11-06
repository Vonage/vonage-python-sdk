# Migration guide from OpenTok Python SDK to Vonage Python SDK

This is a guide to help you migrate from using the OpenTok Python SDK to the Vonage Python SDK to access Video API functionality. You can interact with the Vonage Video API via the Vonage Python SDK to use all the same features available in the `opentok` package.

The OpenTok package includes methods to manage a video application in Python. It includes features like archiving, broadcasting, live captioning and more. All of these features are now available in the Vonage Python SDK, which is the recommended way to access them.

## Contents

- [Improvements](#improvements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Accessing Video API Methods](#accessing-video-api-methods)
- [Accessing Video API Data Models](#accessing-video-api-data-models)
- [New Methods](#new-methods)
- [Changed Methods](#changed-methods)
- [Additional Resources](#additional-resources)

## Improvements

Vonage Video adds data models to help you construct video objects. There's also finer-grained and more descriptive errors. We now authenticate with JWTs, improving security.

You can now manage all your Vonage usage from the Developer Dashboard, including setting callbacks for different video functions as well as things like application configuration and billing.

## Installation

You can now interact with Vonage's Video API using the `vonage-video` PyPI package rather than the `opentok` PyPI package. You shouldn't use this directly for most use cases, it's easier to use the global `vonage` SDK package which includes video functionality. To do this, create a virtual environment and install the `vonage` package in your virtual environment using this command:

```bash
python3 -m venv venv
. ./venv/bin/activate
pip install vonage
```

`vonage-video` will be installed as a dependency so there's no need to install directly.

## Configuration

Whereas the `opentok` package used an `api_key` and `api_secret` for authorization, the Vonage Video API uses JWTs. The SDK handles JWT generation in the background for you, but will require an `application_id` and `private_key` as credentials in order to generate the token. You can obtain these by setting up a Vonage Application, which you can create via the [Developer Dashboard](https://dashboard.nexmo.com/applications). (The Vonage Application is also where you can set other settings such as callback URLs, storage preferences, etc).

These credentials are then passed in when instantiating a `vonage.Vonage` object:

```python
from vonage import Vonage, Auth

vonage_client = Vonage(
	Auth(
		application_id='VONAGE_APPLICATION_ID',
		private_key='VONAGE_PRIVATE_KEY_PATH',
	)
)
```

## Accessing Video API Methods

You can access the Video API via the `Video` class stored at `Vonage.video`. To call methods related to the Video API, use this syntax:

```python
vonage_client.video.video_api_method...
```

## Accessing Video API Data Models

You can access data models for the Video API, e.g. as arguments to video methods, by importing them from the `vonage_video.models` package, e.g.

```python
from vonage_video.models import SessionOptions

session_options = SessionOptions(...)

vonage_client.video.create_session(session_options)
```

## New Methods

`video.list_broadcasts`

## Changed Methods

There are some changes to methods between the `opentok` SDK and the Video API implementation in the `vonage-video` SDK.

- Any positional parameters in method signatures have been replaced with data models in the `vonage-video` package, stored at `vonage_video.models`.
- Methods now return responses as Pydantic data models.
- Some methods have been renamed, for clarity and/or to better reflect what the method does. These are listed below:

| OpenTok Method Name | Vonage Video Method Name |
|---|---|
| `opentok.generate_token` | `video.generate_client_token` |
| `opentok.add_archive_stream` | `video.add_stream_to_archive` |
| `opentok.remove_archive_stream` | `video.remove_stream_from_archive` |
| `opentok.set_archive_layout` | `video.change_archive_layout` |
| `opentok.add_broadcast_stream` | `video.add_stream_to_broadcast` |
| `opentok.remove_broadcast_stream` | `video.remove_stream_from_broadcast` |
| `opentok.set_broadcast_layout` | `video.change_broadcast_layout` |
| `opentok.set_stream_class_lists` | `video.change_stream_layout` |
| `opentok.force_disconnect` | `video.disconnect_client` |
| `opentok.mute_all` | `video.mute_all_streams` |
| `opentok.disable_force_mute` | `video.disable_mute_all_streams`|
| `opentok.dial` | `video.initiate_sip_call`|
| `opentok.start_render` | `video.start_experience_composer`|
| `opentok.list_renders` | `video.list_experience_composers`|
| `opentok.get_render` | `video.get_experience_composer`|
| `opentok.stop_render` | `video.stop_experience_composer`|
| `opentok.connect_audio_to_websocket` | `video.start_audio_connector`|
| `opentok.connect_audio_to_websocket` | `video.start_audio_connector`|

## Additional Resources

- [Vonage Video API Developer Documentation](https://developer.vonage.com/en/video/overview)
- [Vonage Video API Specification](https://developer.vonage.com/en/api/video)
- [Link to the Vonage Python SDK](https://github.com/Vonage/vonage-python-sdk)
- [Join the Vonage Developer Community Slack](https://developer.vonage.com/en/community/slack)
- [Submit a Vonage Video API Support Request](https://api.support.vonage.com/hc/en-us)