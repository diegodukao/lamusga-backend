import os

from unittest.mock import call, patch

import requests
import vcr as vcr_module

from django.conf import settings

from lastfmwrapper import User


vcr = vcr_module.VCR(filter_query_parameters=['api_key'])
cassettes_path = os.path.join(settings.BASE_DIR,
                              'lastfmwrapper/tests/vcr_cassettes/{}')


def test_initializer_user_object():
    username = 'diegodukao'
    lfm_user = User(username)

    expected_params = {
        'api_key': settings.LASTFM_API_KEY,
        'format': 'json',
    }

    assert username == lfm_user.username
    assert 'http://ws.audioscrobbler.com/2.0/' == lfm_user.server
    assert expected_params == lfm_user.request_params


@vcr.use_cassette(cassettes_path.format('user-recent-tracks.yml'))
def test_recent_tracks():
    username = 'diegodukao'
    lfm_user = User(username)

    requests_to_mock_path = 'lastfmwrapper.user.requests.get'
    with patch(requests_to_mock_path, wraps=requests.get) as mock_get:
        response = lfm_user.recent_tracks()

        expected_call = call(
            f'{lfm_user.server}?method=user.getrecenttracks&user={username}',
            params=lfm_user.request_params
        )
        assert expected_call in mock_get.call_args_list

    assert isinstance(response, dict)
    assert set(['track', '@attr']) == response.keys()
    assert response['@attr']['user'] == username
