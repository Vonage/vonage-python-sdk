# Vonage Video API

This package contains the code to use [Vonage's Video API](https://developer.vonage.com/en/video/overview) in Python. This package includes methods for working with video sessions, streams, signals, and more.

## Usage

It is recommended to use this as part of the main `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`.

### Generate a Client Token

```python
from vonage_video.models.token import TokenOptions

token_options = TokenOptions(session_id='your_session_id', role='publisher')
client_token = vonage_client.video.generate_client_token(token_options)
```

### Create a Session

```python
from vonage_video.models.session import SessionOptions

session_options = SessionOptions(media_mode='routed')
video_session = vonage_client.video.create_session(session_options)
```

### List Streams

```python
streams = vonage_client.video.list_streams(session_id='your_session_id')
```

### Get a Stream

```python
stream_info = vonage_client.video.get_stream(session_id='your_session_id', stream_id='your_stream_id')
```

### Change Stream Layout

```python
from vonage_video.models.stream import StreamLayoutOptions

layout_options = StreamLayoutOptions(type='bestFit')
updated_streams = vonage_client.video.change_stream_layout(session_id='your_session_id', stream_layout_options=layout_options)
```

### Send a Signal

```python
from vonage_video.models.signal import SignalData

signal_data = SignalData(type='chat', data='Hello, World!')
vonage_client.video.send_signal(session_id='your_session_id', data=signal_data)
```

### Disconnect a Client

```python
vonage_client.video.disconnect_client(session_id='your_session_id', connection_id='your_connection_id')
```

### Mute a Stream

```python
vonage_client.video.mute_stream(session_id='your_session_id', stream_id='your_stream_id')
```

### Mute All Streams

```python
vonage_client.video.mute_all_streams(session_id='your_session_id', excluded_stream_ids=['stream_id_1', 'stream_id_2'])
```

### Disable Mute All Streams

```python
vonage_client.video.disable_mute_all_streams(session_id='your_session_id')
```

### Start Captions

```python
from vonage_video.models.captions import CaptionsOptions

captions_options = CaptionsOptions(language='en-US')
captions_data = vonage_client.video.start_captions(captions_options)
```

### Stop Captions

```python
from vonage_video.models.captions import CaptionsData

captions_data = CaptionsData(captions_id='your_captions_id')
vonage_client.video.stop_captions(captions_data)
```

### Start Audio Connector

```python
from vonage_video.models.audio_connector import AudioConnectorOptions

audio_connector_options = AudioConnectorOptions(session_id='your_session_id', token='your_token', url='https://example.com')
audio_connector_data = vonage_client.video.start_audio_connector(audio_connector_options)
```

### Start Experience Composer

```python
from vonage_video.models.experience_composer import ExperienceComposerOptions

experience_composer_options = ExperienceComposerOptions(session_id='your_session_id', token='your_token', url='https://example.com')
experience_composer = vonage_client.video.start_experience_composer(experience_composer_options)
```
