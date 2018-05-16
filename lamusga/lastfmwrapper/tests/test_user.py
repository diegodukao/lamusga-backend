from lastfmwrapper import User


def test_user_recent_tracks():
    lfm_user = User('diegodukao')
    response = lfm_user.recent_tracks()

    assert isinstance(response, dict)
