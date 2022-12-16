basic_notify = '{"payload": {"message": "hello"}, "eventUrl": ["http://example.com"], "action": "notify"}'

full_notify = (
    '{"payload": {"message": "hello"}, "eventUrl": ["http://example.com"], "eventMethod": "POST", "action": "notify"}'
)

two_notify_ncco = '[{"action": "notify", "payload": {"message": "hello"}, "eventUrl": ["http://example.com"]}, {"action": "notify", "payload": {"message": "world"}, "eventUrl": ["http://example.com"], "eventMethod": "PUT"}]'

basic_talk = '{"action": "talk"}'

full_talk = (
    '{"bargeIn": true, "loop": 3, "level": 0.5, "language": "en-GB", "style": 1, "premium": true, "action": "talk"}'
)
