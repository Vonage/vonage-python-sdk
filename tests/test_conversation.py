#!/usr/bin/env python

import json
from util import *

import nexmo


@responses.activate
def test_create_conversation(client, dummy_data, auth):
    stub(
        responses.POST,
        "https://api.nexmo.com/v0.1/conversations",
        fixture_path="conversations/create_conversation.json",
    )

    conversation = client.conversation.create_conversation(
        {"name": "conversation-2", "display_name": "My Super Conversation"}
    )
    auth.assert_jwt_auth()
    assert isinstance(conversation, dict)
    assert conversation["id"] == "CON-afe887d8-d587-4280-9aae-dfa4c9227d5e"
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_list_conversations(client, dummy_data, auth):
    stub(
        responses.GET,
        "https://api.nexmo.com/v0.1/conversations",
        fixture_path="conversations/list_conversations.json",
    )

    conversations = client.conversation.list_conversations()
    auth.assert_jwt_auth()
    assert isinstance(conversations, dict)
    assert conversations["page_size"] == 10
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_get_conversation(client, dummy_data, auth):
    stub(
        responses.GET,
        "https://api.nexmo.com/v0.1/conversations/CON-afe887d8-d587-4280-9aae-dfa4c9227d5e",
        fixture_path="conversations/get_conversation.json",
    )

    conversation = client.conversation.get_conversation(
        "CON-afe887d8-d587-4280-9aae-dfa4c9227d5e"
    )
    auth.assert_jwt_auth()
    assert isinstance(conversation, dict)
    assert conversation["id"] == "CON-afe887d8-d587-4280-9aae-dfa4c9227d5e"
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_update_conversation(client, dummy_data, auth):
    stub(
        responses.PUT,
        "https://api.nexmo.com/v0.1/conversations/CON-afe887d8-d587-4280-9aae-dfa4c9227d5e",
        fixture_path="conversations/update_conversation.json",
    )

    conversation = client.conversation.update_conversation(
        {"id": "CON-afe887d8-d587-4280-9aae-dfa4c9227d5e"}
    )
    auth.assert_jwt_auth()
    assert isinstance(conversation, dict)
    assert conversation["id"] == "CON-afe887d8-d587-4280-9aae-dfa4c9227d5e"

    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_delete_conversation(client, dummy_data, auth):
    stub(
        responses.DELETE,
        "https://api.nexmo.com/v0.1/conversations/CON-afe887d8-d587-4280-9aae-dfa4c9227d5e",
        status_code=204,
    )

    response = client.conversation.delete_conversation(
        "CON-afe887d8-d587-4280-9aae-dfa4c9227d5e"
    )
    auth.assert_jwt_auth()
    assert response is None
    assert request_user_agent() == dummy_data.user_agent


# User tests ==========================================================


@responses.activate
def test_create_user(client, dummy_data, auth):
    stub(
        responses.POST,
        "https://api.nexmo.com/v0.1/users",
        fixture_path="conversations/create_user.json",
    )

    user = client.conversation.create_user(
        {"name": "conversation-2", "display_name": "My Super Conversation"}
    )
    auth.assert_jwt_auth()
    assert isinstance(user, dict)
    assert user["id"] == "USR-e46d9542-752a-4786-8f12-25a2e623a793"
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_list_users(client, dummy_data, auth):
    stub(
        responses.GET,
        "https://api.nexmo.com/v0.1/users",
        fixture_path="conversations/list_users.json",
    )

    users = client.conversation.list_users()
    auth.assert_jwt_auth()
    assert isinstance(users, dict)
    assert users["page_size"] == 10
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_get_user(client, dummy_data, auth):
    stub(
        responses.GET,
        "https://api.nexmo.com/v0.1/users/USR-e46d9542-752a-4786-8f12-25a2e623a793",
        fixture_path="conversations/get_user.json",
    )

    user = client.conversation.get_user("USR-e46d9542-752a-4786-8f12-25a2e623a793")
    auth.assert_jwt_auth()
    assert isinstance(user, dict)
    assert user["id"] == "USR-e46d9542-752a-4786-8f12-25a2e623a793"
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_update_user(client, dummy_data, auth):
    stub(
        responses.PUT,
        "https://api.nexmo.com/v0.1/users/USR-e46d9542-752a-4786-8f12-25a2e623a793",
        fixture_path="conversations/update_user.json",
    )

    user = client.conversation.update_user(
        {"id": "USR-e46d9542-752a-4786-8f12-25a2e623a793"}
    )
    auth.assert_jwt_auth()
    assert isinstance(user, dict)
    assert user["id"] == "USR-e46d9542-752a-4786-8f12-25a2e623a793"

    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_delete_user(client, dummy_data, auth):
    stub(
        responses.DELETE,
        "https://api.nexmo.com/v0.1/users/USR-e46d9542-752a-4786-8f12-25a2e623a793",
        status_code=204,
    )

    response = client.conversation.delete_user(
        "USR-e46d9542-752a-4786-8f12-25a2e623a793"
    )
    auth.assert_jwt_auth()
    assert response is None
    assert request_user_agent() == dummy_data.user_agent


# Member tests =====================================


@responses.activate
def test_create_member(client, dummy_data, auth):
    stub(
        responses.POST,
        "https://api.nexmo.com/v0.1/conversations/CON-afe887d8-d587-4280-9aae-dfa4c9227d5e/members",
        fixture_path="conversations/create_member.json",
    )

    member = client.conversation.create_member(
        "CON-afe887d8-d587-4280-9aae-dfa4c9227d5e",
        {"user_id": "USR-e46d9542-752a-4786-8f12-25a2e623a793"},
    )
    auth.assert_jwt_auth()
    assert isinstance(member, dict)
    assert member["id"] == "MEM-afe887d8-d587-4280-9aae-dfa4c9227d5e"
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_list_members(client, dummy_data, auth):
    stub(
        responses.GET,
        "https://api.nexmo.com/v0.1/conversations/CON-afe887d8-d587-4280-9aae-dfa4c9227d5e/members",
        fixture_path="conversations/list_members.json",
    )

    members = client.conversation.list_members(
        "CON-afe887d8-d587-4280-9aae-dfa4c9227d5e"
    )
    auth.assert_jwt_auth()
    assert isinstance(members, dict)
    assert members["page_size"] == 10
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_get_member(client, dummy_data, auth):
    stub(
        responses.GET,
        "https://api.nexmo.com/v0.1/conversations/CON-afe887d8-d587-4280-9aae-dfa4c9227d5e/members/MEM-afe887d8-d587-4280-9aae-dfa4c9227d5e",
        fixture_path="conversations/get_member.json",
    )

    member = client.conversation.get_member(
        "CON-afe887d8-d587-4280-9aae-dfa4c9227d5e",
        "MEM-afe887d8-d587-4280-9aae-dfa4c9227d5e",
    )
    auth.assert_jwt_auth()
    assert isinstance(member, dict)
    assert member["id"] == "MEM-afe887d8-d587-4280-9aae-dfa4c9227d5e"
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_update_member(client, dummy_data, auth):
    stub(
        responses.PUT,
        "https://api.nexmo.com/v0.1/conversations/CON-afe887d8-d587-4280-9aae-dfa4c9227d5e/members/MEM-afe887d8-d587-4280-9aae-dfa4c9227d5e",
        fixture_path="conversations/update_member.json",
    )

    member = client.conversation.update_member(
        "CON-afe887d8-d587-4280-9aae-dfa4c9227d5e",
        "MEM-afe887d8-d587-4280-9aae-dfa4c9227d5e",
        {"user_id": "USR-e46d9542-752a-4786-8f12-25a2e623a793"},
    )
    auth.assert_jwt_auth()
    assert isinstance(member, dict)
    assert member["id"] == "MEM-afe887d8-d587-4280-9aae-dfa4c9227d5e"

    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_delete_member(client, dummy_data, auth):
    stub(
        responses.DELETE,
        "https://api.nexmo.com/v0.1/conversations/CON-afe887d8-d587-4280-9aae-dfa4c9227d5e/members/MEM-afe887d8-d587-4280-9aae-dfa4c9227d5e",
        status_code=204,
    )

    response = client.conversation.delete_member(
        "CON-afe887d8-d587-4280-9aae-dfa4c9227d5e",
        "MEM-afe887d8-d587-4280-9aae-dfa4c9227d5e",
    )
    auth.assert_jwt_auth()
    assert response is None
    assert request_user_agent() == dummy_data.user_agent


# Event tests ======================================


@responses.activate
def test_create_event(client, dummy_data, auth):
    stub(
        responses.POST,
        "https://api.nexmo.com/v0.1/conversations/CON-afe887d8-d587-4280-9aae-dfa4c9227d5e/events",
        fixture_path="conversations/create_event.json",
    )

    event = client.conversation.create_event(
        "CON-afe887d8-d587-4280-9aae-dfa4c9227d5e",
        {
            "type": "text",
            "body": {"text": "This is my message."},
            "to": "MEM-afe887d8-d587-4280-9aae-dfa4c9227d5e",
            "from": "MEM-e46d9542-752a-4786-8f12-25a2e623a793",
        },
    )
    auth.assert_jwt_auth()
    assert isinstance(event, dict)
    assert event["id"] == 9
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_list_events(client, dummy_data, auth):
    stub(
        responses.GET,
        "https://api.nexmo.com/v0.1/conversations/CON-afe887d8-d587-4280-9aae-dfa4c9227d5e/events",
        fixture_path="conversations/list_events.json",
    )

    events = client.conversation.list_events(
        "CON-afe887d8-d587-4280-9aae-dfa4c9227d5e", start_id=13, end_id=19
    )
    auth.assert_jwt_auth()
    assert isinstance(events, dict)
    assert events["page_size"] == 10
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_get_event(client, dummy_data, auth):
    stub(
        responses.GET,
        "https://api.nexmo.com/v0.1/conversations/CON-afe887d8-d587-4280-9aae-dfa4c9227d5e/events/9",
        fixture_path="conversations/get_event.json",
    )

    event = client.conversation.get_event("CON-afe887d8-d587-4280-9aae-dfa4c9227d5e", 9)
    auth.assert_jwt_auth()
    assert isinstance(event, dict)
    assert event["id"] == 9
    assert request_user_agent() == dummy_data.user_agent


@responses.activate
def test_delete_event(client, dummy_data, auth):
    stub(
        responses.DELETE,
        "https://api.nexmo.com/v0.1/conversations/CON-afe887d8-d587-4280-9aae-dfa4c9227d5e/events/9",
        status_code=204,
    )

    response = client.conversation.delete_event(
        "CON-afe887d8-d587-4280-9aae-dfa4c9227d5e", 9
    )
    auth.assert_jwt_auth()
    assert response is None
    assert request_user_agent() == dummy_data.user_agent
