from vonage import Client, ProactiveConnect
from util import *

import responses

proc = ProactiveConnect(Client(application_id='my_app', private_key='my_key'))


@responses.activate
def test_list_all_lists():
    stub(
        responses.GET,
        'https://api-eu.vonage.com/v0.1/bulk/lists',
        fixture_path='proactive_connect/list_lists.json',
    )

    lists = proc.list_all_lists()
    assert lists[0] == True
