record_full = '{"action": "record", "format": "wav", "split": "conversation", "channels": 4, "endOnSilence": 5, "endOnKey": "*", "timeOut": 100, "beepStart": true, "eventUrl": ["http://example.com"], "eventMethod": "PUT"}'

record_url_as_str = '{"action": "record", "eventUrl": ["http://example.com/events"]}'

record_add_split = '{"action": "record", "split": "conversation", "channels": 4}'

conversation_basic = '{"action": "notify", "name": "my_conversation"}'

conversation_full = '{"action": "notify", "name": "my_conversation", "musicOnHoldUrl": ["http://example.com/music.mp3"], "startOnEnter": true, "endOnExit": true, "record": true, "canSpeak": ["asdf", "qwer"], "canHear": ["asdf"]}'

conversation_mute_option = '{"action": "notify", "name": "my_conversation", "mute": true}'

talk_basic = '{"action": "talk", "text": "hello"}'

talk_full = '{"action": "talk", "text": "hello", "bargeIn": true, "loop": 3, "level": 0.5, "language": "en-GB", "style": 1, "premium": true}'

notify_basic = '{"action": "notify", "payload": {"message": "hello"}, "eventUrl": ["http://example.com"]}'

notify_full = (
    '{"action": "notify", "payload": {"message": "hello"}, "eventUrl": ["http://example.com"], "eventMethod": "POST"}'
)

two_notify_ncco = '[{"action": "notify", "payload": {"message": "hello"}, "eventUrl": ["http://example.com"]}, {"action": "notify", "payload": {"message": "world"}, "eventUrl": ["http://example.com"], "eventMethod": "PUT"}]'
