# Vonage Video API

This package contains the code to use [Vonage's Video API](https://developer.vonage.com/en/video/overview) in Python. This package includes methods for working with video sessions, streams, signals, and more.

## Usage

It is recommended to use this as part of the main `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`.

You will use the custom Pydantic data models to make most of the API calls in this package.

### Generate a Client Token

```python
from vonage_video import TokenOptions

token_options = TokenOptions(session_id='your_session_id', role='publisher')
client_token = vonage_client.video.generate_client_token(token_options)
```

### Create a Session

```python
from vonage_video import SessionOptions

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
from vonage_video import StreamLayoutOptions

layout_options = StreamLayoutOptions(type='bestFit')
updated_streams = vonage_client.video.change_stream_layout(session_id='your_session_id', stream_layout_options=layout_options)
```

### Send a Signal

```python
from vonage_video import SignalData

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
from vonage_video import CaptionsOptions

captions_options = CaptionsOptions(language='en-US')
captions_data = vonage_client.video.start_captions(captions_options)
```

### Stop Captions

```python
from vonage_video import CaptionsData

captions_data = CaptionsData(captions_id='your_captions_id')
vonage_client.video.stop_captions(captions_data)
```

### Start Audio Connector

```python
from vonage_video import AudioConnectorOptions

audio_connector_options = AudioConnectorOptions(session_id='your_session_id', token='your_token', url='https://example.com')
audio_connector_data = vonage_client.video.start_audio_connector(audio_connector_options)
```

### Start Experience Composer

```python
from vonage_video import ExperienceComposerOptions

experience_composer_options = ExperienceComposerOptions(session_id='your_session_id', token='your_token', url='https://example.com')
experience_composer = vonage_client.video.start_experience_composer(experience_composer_options)
```

### List Experience Composers

```python
from vonage_video import ListExperienceComposersFilter

filter = ListExperienceComposersFilter(page_size=10)
experience_composers, count, next_page_offset = vonage_client.video.list_experience_composers(filter)
print(experience_composers)
```

### Get Experience Composer

```python
experience_composer = vonage_client.video.get_experience_composer(experience_composer_id='experience_composer_id')
```

### Stop Experience Composer

```python
vonage_client.video.stop_experience_composer(experience_composer_id='experience_composer_id')
```

### List Archives

```python
from vonage_video import ListArchivesFilter

filter = ListArchivesFilter(offset=2)
archives, count, next_page_offset = vonage_client.video.list_archives(filter)
print(archives)
```

### Start Archive

```python
from vonage_video import CreateArchiveRequest

archive_options = CreateArchiveRequest(session_id='your_session_id', name='My Archive')
archive = vonage_client.video.start_archive(archive_options)
```

### Get Archive

```python
archive = vonage_client.video.get_archive(archive_id='your_archive_id')
print(archive)
```

### Delete Archive

```python
vonage_client.video.delete_archive(archive_id='your_archive_id')
```

### Add Stream to Archive

```python
from vonage_video import AddStreamRequest

add_stream_request = AddStreamRequest(stream_id='your_stream_id')
vonage_client.video.add_stream_to_archive(archive_id='your_archive_id', params=add_stream_request)
```

### Remove Stream from Archive

```python
vonage_client.video.remove_stream_from_archive(archive_id='your_archive_id', stream_id='your_stream_id')
```

### Stop Archive

```python
archive = vonage_client.video.stop_archive(archive_id='your_archive_id')
print(archive)
```

### Change Archive Layout

```python
from vonage_video import ComposedLayout

layout = ComposedLayout(type='bestFit')
archive = vonage_client.video.change_archive_layout(archive_id='your_archive_id', layout=layout)
print(archive)
```

### List Broadcasts

```python
from vonage_video import ListBroadcastsFilter

filter = ListBroadcastsFilter(page_size=10)
broadcasts, count, next_page_offset = vonage_client.video.list_broadcasts(filter)
print(broadcasts)
```

### Start Broadcast

```python
from vonage_video import CreateBroadcastRequest, BroadcastOutputSettings, BroadcastHls, BroadcastRtmp

broadcast_options = CreateBroadcastRequest(session_id='your_session_id', outputs=BroadcastOutputSettings(
    hls=BroadcastHls(dvr=True, low_latency=False),
    rtmp=[
        BroadcastRtmp(
            id='test',
            server_url='rtmp://a.rtmp.youtube.com/live2',
            stream_name='stream-key',
        )
    ],
)
)
broadcast = vonage_client.video.start_broadcast(broadcast_options)
print(broadcast)
```

### Get Broadcast

```python
broadcast = vonage_client.video.get_broadcast(broadcast_id='your_broadcast_id')
print(broadcast)
```

### Stop Broadcast

```python
broadcast = vonage_client.video.stop_broadcast(broadcast_id='your_broadcast_id')
print(broadcast)
```

### Change Broadcast Layout

```python
from vonage_video import ComposedLayout

layout = ComposedLayout(type='bestFit')
broadcast = vonage_client.video.change_broadcast_layout(broadcast_id='your_broadcast_id', layout=layout)
print(broadcast)
```

### Add Stream to Broadcast

```python
from vonage_video import AddStreamRequest

add_stream_request = AddStreamRequest(stream_id='your_stream_id')
vonage_client.video.add_stream_to_broadcast(broadcast_id='your_broadcast_id', params=add_stream_request)
```

### Remove Stream from Broadcast

```python
vonage_client.video.remove_stream_from_broadcast(broadcast_id='your_broadcast_id', stream_id='your_stream_id')
```

### Initiate SIP Call

```python
from vonage_video import InitiateSipRequest, SipOptions, SipAuth

sip_request_params = InitiateSipRequest(
    session_id='your_session_id',
    token='your_token',
    sip=SipOptions(
        uri=f'sip:{vonage_number}@sip.nexmo.com;transport=tls',
        from_=f'test@vonage.com',
        headers={'header_key': 'header_value'},
        auth=SipAuth(username='1485b9e6', password='fL8jvi4W2FmS9som'),
        secure=False,
        video=False,
        observe_force_mute=True,
    ),
)
sip_call = vonage_client.video.initiate_sip_call(sip_request_params)
print(sip_call)
```

### Play DTMF into a call

```python
# Play into all connections
session_id = 'your_session_id'
digits = '1234#*p'

vonage_client.video.play_dtmf(session_id=session_id, digits=digits)

# Play into one connection
session_id = 'your_session_id'
digits = '1234#*p'
connection_id = 'your_connection_id'

vonage_client.video.play_dtmf(session_id=session_id, digits=digits, connection_id=connection_id)
```