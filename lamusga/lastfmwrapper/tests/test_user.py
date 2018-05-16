import os

import vcr as vcr_module
from django.conf import settings

from lastfmwrapper import User


vcr = vcr_module.VCR(filter_query_parameters=['api_key'])
cassettes_path = os.path.join(settings.BASE_DIR,
                              'lastfmwrapper/tests/vcr_cassettes/{}')


@vcr.use_cassette(cassettes_path.format('user-recent-tracks.yml'))
def test_recent_tracks():
    username = 'diegodukao'
    lfm_user = User(username)
    response = lfm_user.recent_tracks()

    assert isinstance(response, dict)
    assert set(['track', '@attr']) == response.keys()
    assert response['@attr']['user'] == username
