import base64

import requests

from django.conf import settings


class Auth(object):

    def __init__(self, code):
        self.code = code
        self.redirect_uri = settings.SPOTIFY_REDIRECT_URI

        client_id = settings.SPOTIFY_CLIENT_ID
        client_secret = settings.SPOTIFY_CLIENT_SECRET
        auth_key = base64.b64encode(
            f'{client_id}:{client_secret}'.encode('ascii'))
        self.auth_key = auth_key.decode('ascii')

        self.url = 'https://accounts.spotify.com/api/token'

    @property
    def _headers(self):
        return {
            'Content-Type': 'application/x-www-form-urlencoded',
            'Authorization': f'Basic {self.auth_key}',
        }

    def request_tokens(self):
        payload = {
            'grant_type': 'authorization_code',
            'code': self.code,
            'redirect_uri': self.redirect_uri,
          }

        response = requests.post(
            self.url, headers=self._headers, data=payload)
        data = response.json()

        return data['access_token'], data['refresh_token']
