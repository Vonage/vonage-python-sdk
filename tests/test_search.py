from util import *


@responses.activate
def test_get_message(client, dummy_data):
    stub(responses.GET, "https://rest.nexmo.com/search/message")

    assert isinstance(client.get_message("00A0B0C0"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "id=00A0B0C0" in request_query()


@responses.activate
def test_get_message_rejections(client, dummy_data):
    stub(responses.GET, "https://rest.nexmo.com/search/rejections")

    assert isinstance(client.get_message_rejections(date="YYYY-MM-DD"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "date=YYYY-MM-DD" in request_query()


@responses.activate
def test_search_messages(client, dummy_data):
    stub(responses.GET, "https://rest.nexmo.com/search/messages")

    assert isinstance(client.search_messages(to="1234567890", date="YYYY-MM-DD"), dict)
    assert request_user_agent() == dummy_data.user_agent
    assert "date=YYYY-MM-DD" in request_query()
    assert "to=1234567890" in request_query()


@responses.activate
def test_search_messages_by_ids(client, dummy_data):
    stub(responses.GET, "https://rest.nexmo.com/search/messages")

    assert isinstance(
        client.search_messages(ids=["00A0B0C0", "00A0B0C1", "00A0B0C2"]), dict
    )
    assert request_user_agent() == dummy_data.user_agent
    assert "ids=00A0B0C0" in request_query()
    assert "ids=00A0B0C1" in request_query()
    assert "ids=00A0B0C2" in request_query()
