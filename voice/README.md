# Vonage Voice Package

This package contains the code to use [Vonage's Voice API](https://developer.vonage.com/en/voice/voice-api/overview) in Python. This package includes methods for working with the Voice API. It also contains an NCCO (Call Control Object) builder to help you to control call flow.

## Structure

There is a `Voice` class which contains the methods used to call Vonage APIs. To call many of the APIs, you need to pass a Pydantic model with the required options. Errors can be accessed from the `vonage_voice.errors` module.

## Usage

It is recommended to use this as part of the main `vonage` package. The examples below assume you've created an instance of the `vonage.Vonage` class called `vonage_client`, like so:

```python
from vonage import Vonage, Auth

vonage_client = Vonage(Auth('MY_AUTH_INFO'))
```

### Create a Call

To create a call, you must pass an instance of the `CreateCallRequest` model to the `create_call` method. If supplying an NCCO, import the NCCO actions you want to use and pass them in as a list to the `ncco` model field.

```python
from vonage_voice import CreateCallRequest, Talk

ncco = [Talk(text='Hello world', loop=3, language='en-GB')]

call = CreateCallRequest(
    to=[{'type': 'phone', 'number': '1234567890'}],
    ncco=ncco,
    random_from_number=True,
)

response = vonage_client.voice.create_call(call)
print(response.model_dump())
```

### List Calls

```python
# Gets the first 100 results and the record_index of the
# next page if there's more than 100
calls, next_record_index = vonage_client.voice.list_calls()

# Specify filtering options
from vonage_voice import ListCallsFilter

call_filter = ListCallsFilter(
    status='completed',
    date_start='2024-03-14T07:45:14Z',
    date_end='2024-04-19T08:45:14Z',
    page_size=10,
    record_index=0,
    order='asc',
    conversation_uuid='CON-2be039b2-d0a4-4274-afc8-d7b241c7c044',
)

calls, next_record_index = vonage_client.voice.list_calls(call_filter)
```

### Get Information About a Specific Call

```python
call = vonage_client.voice.get_call('CALL_ID')
```

### Transfer a Call to a New NCCO

```python
ncco = [Talk(text='Hello world')]
vonage_client.voice.transfer_call_ncco('UUID', ncco)
```

### Transfer a Call to a New Answer URL

```python
vonage_client.voice.transfer_call_answer_url('UUID', 'ANSWER_URL')
```

### Hang Up a Call

End the call for a specified UUID, removing them from it.

```python
vonage_client.voice.hangup('UUID')
```

### Mute/Unmute a Participant

```python
vonage_client.voice.mute('UUID')
vonage_client.voice.unmute('UUID')
```

### Earmuff/Unearmuff a UUID

Prevent/allow a specified UUID participant to be able to hear audio.

```python
vonage_client.voice.earmuff('UUID')
vonage_client.voice.unearmuff('UUID')
```

### Play Audio Into a Call

```python
from vonage_voice import AudioStreamOptions

# Only the `stream_url` option is required
options = AudioStreamOptions(
    stream_url=['https://example.com/audio'], loop=2, level=0.5
)
response = vonage_client.voice.play_audio_into_call('UUID', options)
```

### Stop Playing Audio Into a Call

```python
vonage_client.voice.stop_audio_stream('UUID')
```

### Play TTS Into a Call

```python
from vonage_voice import TtsStreamOptions

# Only the `text` field is required
options = TtsStreamOptions(
    text='Hello world', language='en-ZA', style=1, premium=False, loop=2, level=0.5
)
response = voice.play_tts_into_call('UUID', options)
```

### Stop Playing TTS Into a Call

```python
vonage_client.voice.stop_tts('UUID')
```

### Play DTMF Tones Into a Call

```python
response = voice.play_dtmf_into_call('UUID', '1234*#')
```