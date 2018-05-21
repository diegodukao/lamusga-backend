import base64

import requests

from django.conf import settings

from spotifywrapper.exceptions import NoCodeNeitherRefreshTokenException


class Auth(object):
    '''
    Class that handles Spotify authentication. When initializing an auth
    object, `code` is needed for requesting access and refresh tokens
    and `refresh_token` is needed for refreshing the access token.
    '''

    def __init__(self, code=None, refresh_token=None):
        self.code = code
        self.refresh_token = refresh_token
        if not self.code and not self.refresh_token:
            msg = ("You need to pass the auth code or the refresh token "
                   "to create an Auth object")
            raise NoCodeNeitherRefreshTokenException(msg)

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

    def refresh_access_token(self):
        payload = {
            'grant_type': 'refresh_token',
            'refresh_token': self.refresh_token,
        }

        response = requests.post(
            self.url, headers=self._headers, data=payload)
        data = response.json()

        return data['access_token']
