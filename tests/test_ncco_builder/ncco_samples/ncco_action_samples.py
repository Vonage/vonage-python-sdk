record_full = '{"action": "record", "format": "wav", "split": "conversation", "channels": 4, "endOnSilence": 5, "endOnKey": "*", "timeOut": 100, "beepStart": true, "eventUrl": ["http://example.com"], "eventMethod": "PUT"}'

record_url_as_str = '{"action": "record", "eventUrl": ["http://example.com/events"]}'

record_add_split = '{"action": "record", "split": "conversation", "channels": 4}'

conversation_basic = '{"action": "conversation", "name": "my_conversation"}'

conversation_full = '{"action": "conversation", "name": "my_conversation", "musicOnHoldUrl": ["http://example.com/music.mp3"], "startOnEnter": true, "endOnExit": true, "record": true, "canSpeak": ["asdf", "qwer"], "canHear": ["asdf"]}'

conversation_mute_option = '{"action": "conversation", "name": "my_conversation", "mute": true}'

connect_phone = '{"action": "connect", "endpoint": [{"type": "phone", "number": "447000000000", "dtmfAnswer": "1p2p3p#**903#", "onAnswer": {"url": "https://example.com/answer", "ringbackTone": "http://example.com/ringbackTone.wav"}}]}'

connect_app = '{"action": "connect", "endpoint": [{"type": "app", "user": "test_user"}]}'

connect_websocket = '{"action": "connect", "endpoint": [{"type": "websocket", "uri": "ws://example.com/socket", "contentType": "audio/l16;rate=8000", "headers": {"language": "en-GB"}}]}'

connect_sip = '{"action": "connect", "endpoint": [{"type": "sip", "uri": "sip:rebekka@sip.mcrussell.com", "headers": {"location": "New York City", "occupation": "developer"}}]}'

connect_vbc = '{"action": "connect", "endpoint": [{"type": "vbc", "extension": "111"}]}'

connect_full = '{"action": "connect", "endpoint": [{"type": "phone", "number": "447000000000"}], "from": "447400000000", "randomFromNumber": false, "eventType": "synchronous", "timeout": 15, "limit": 1000, "machineDetection": "hangup", "eventUrl": ["http://example.com"], "eventMethod": "PUT", "ringbackTone": "http://example.com"}'

connect_advancedMachineDetection = '{"action": "connect", "endpoint": [{"type": "phone", "number": "447000000000"}], "from": "447400000000", "advancedMachineDetection": {"behavior": "continue", "mode": "detect"}, "eventUrl": ["http://example.com"]}'

talk_basic = '{"action": "talk", "text": "hello"}'

talk_full = '{"action": "talk", "text": "hello", "bargeIn": true, "loop": 3, "level": 0.5, "language": "en-GB", "style": 1, "premium": true}'

stream_basic = '{"action": "stream", "streamUrl": ["https://example.com/stream/music.mp3"]}'

stream_full = '{"action": "stream", "streamUrl": ["https://example.com/stream/music.mp3"], "level": 0.1, "bargeIn": true, "loop": 10}'

input_basic_dtmf = '{"action": "input", "type": ["dtmf"]}'

input_basic_dtmf_speech = '{"action": "input", "type": ["dtmf", "speech"]}'

input_dtmf_and_speech_full = '{"action": "input", "type": ["dtmf", "speech"], "dtmf": {"timeOut": 5, "maxDigits": 12, "submitOnHash": true}, "speech": {"uuid": "my-uuid", "endOnSilence": 2.5, "language": "en-GB", "context": ["sales", "billing"], "startTimeout": 20, "maxDuration": 30, "saveAudio": true}, "eventUrl": ["http://example.com/speech"], "eventMethod": "PUT"}'

notify_basic = '{"action": "notify", "payload": {"message": "hello"}, "eventUrl": ["http://example.com"]}'

notify_full = (
    '{"action": "notify", "payload": {"message": "hello"}, "eventUrl": ["http://example.com"], "eventMethod": "POST"}'
)

pay_basic = '{"action": "pay", "amount": 10.0}'

pay_voice_full = '{"action": "pay", "amount": 99.99, "currency": "gbp", "eventUrl": ["https://example.com/payment"], "voice": {"language": "en-GB", "style": 1}}'

pay_text = '{"action": "pay", "amount": 12.35, "currency": "gbp", "eventUrl": ["https://example.com/payment"], "prompts": {"type": "CardNumber", "text": "Enter your card number.", "errors": {"InvalidCardType": {"text": "The card you are trying to use is not valid for this purchase."}}}}'

pay_text_multiple_prompts = '{"action": "pay", "amount": 12.0, "prompts": [{"type": "CardNumber", "text": "Enter your card number.", "errors": {"InvalidCardType": {"text": "The card you are trying to use is not valid for this purchase."}}}, {"type": "ExpirationDate", "text": "Enter your card expiration date.", "errors": {"InvalidExpirationDate": {"text": "You have entered an invalid expiration date."}, "Timeout": {"text": "Please enter your card\'s expiration date."}}}, {"type": "SecurityCode", "text": "Enter your 3-digit security code.", "errors": {"InvalidSecurityCode": {"text": "You have entered an invalid security code."}, "Timeout": {"text": "Please enter your card\'s security code."}}}]}'

two_notify_ncco = '[{"action": "notify", "payload": {"message": "hello"}, "eventUrl": ["http://example.com"]}, {"action": "notify", "payload": {"message": "world"}, "eventUrl": ["http://example.com"], "eventMethod": "PUT"}]'
