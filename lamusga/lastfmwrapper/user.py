import requests

from django.conf import settings


class User(object):

    def __init__(self, username):
        self.username = username
        self.server = 'http://ws.audioscrobbler.com/2.0/'

        self.request_params = {
            'api_key': settings.LASTFM_API_KEY,
            'format': 'json',
        }

    def recent_tracks(self):
        path = (
            f'{self.server}'
            f'?method=user.getrecenttracks'
            f'&user={self.username}'
        )
        response = requests.get(
            path,
            params=self.request_params
        )
        data = response.json()
        return data['recenttracks']
