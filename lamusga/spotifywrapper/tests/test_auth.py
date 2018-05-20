import base64
import os

import vcr as vcr_module

from django.conf import settings

from spotifywrapper import Auth


vcr = vcr_module.VCR(filter_headers=['Authorization'])
cassettes_path = os.path.join(settings.BASE_DIR,
                              'spotifywrapper/tests/vcr_cassettes/{}')


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


def test_headers_property():
    code = 'coDE'
    spfy_auth = Auth(code)

    fake_auth_key = 'fake_key'
    spfy_auth.auth_key = fake_auth_key

    headers = spfy_auth._headers
    assert isinstance(headers, dict)
    assert 'application/x-www-form-urlencoded' == headers['Content-Type']
    assert f'Basic {fake_auth_key}' == headers['Authorization']


@vcr.use_cassette(cassettes_path.format('auth_request_tokens.yml'))
def test_request_access_and_refresh_tokens():
    code = 'AQBIEf9hzHiP2NyDYbX5uheTqeYj8goASVdGHqz1-w7h3JXipOwSRbBxuA4XFq4blfeZuOHTIX0c1v4wtMK2pKN9dDcFis2CYuSNoJPjWeaRRPIA76tXeFoc60l1PQTZdF772EJZThWUGaEh9JLb98AD1JUkoqK2PdhUDPA2be5TtQUvu33r1vZsWHItuw7Ta-NRqtqUuQ3I_pevhdc94rIMHu05Ub5pHda9UN3WYRg-_u5FYVRvxA'  # NOQA
    spfy_auth = Auth(code)
    access_token, refresh_token = spfy_auth.request_tokens()

    assert access_token
    assert refresh_token
