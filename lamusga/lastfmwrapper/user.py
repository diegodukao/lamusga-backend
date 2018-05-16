from lastfmwrapper import session  # created in __init__.py


class User(object):

    def __init__(self, username):
        self.username = username
        self.server = 'http://ws.audioscrobbler.com/2.0/'

    def recent_tracks(self):
        path = self.server + '?method=user.getrecenttracks&user={}'
        response = session.get(path.format(self.username))
        data = response.json()
        return data['recenttracks']
