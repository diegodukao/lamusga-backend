import vcr

from lastfmwrapper import User


@vcr.use_cassette('vcr_cassettes/user-recent-tracks.yml')
def test_recent_tracks():
    username = 'diegodukao'
    lfm_user = User(username)
    response = lfm_user.recent_tracks()

    assert isinstance(response, dict)
    assert set(['track', '@attr']) == response.keys()
    assert response['@attr']['user'] == username
