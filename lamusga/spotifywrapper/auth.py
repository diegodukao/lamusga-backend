import base64

from django.conf import settings


class Auth(object):

    def __init__(self, code):
        self.code = code
        self.redirect_uri = settings.SPOTIFY_REDIRECT_URI

        client_id = settings.SPOTIFY_CLIENT_ID
        client_secret = settings.SPOTIFY_CLIENT_SECRET
        bearer = base64.b64encode(
            f'{client_id}:{client_secret}'.encode('ascii'))
        self.bearer = bearer.decode('ascii')
