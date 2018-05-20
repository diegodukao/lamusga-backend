import base64

from django.conf import settings

from spotifywrapper import Auth


def test_initialize_auth_object():
    code = 'coDE'
    spfy_auth = Auth(code)

    client_id = settings.SPOTIFY_CLIENT_ID
    client_secret = settings.SPOTIFY_CLIENT_SECRET
    expected_auth_key = base64.b64encode(
        f'{client_id}:{client_secret}'.encode('ascii')).decode('ascii')

    assert code == spfy_auth.code
    assert settings.SPOTIFY_REDIRECT_URI == spfy_auth.redirect_uri
    assert expected_auth_key == spfy_auth.auth_key
