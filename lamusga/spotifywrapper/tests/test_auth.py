import base64
import os

from unittest.mock import call, patch

import pytest
import requests
import vcr as vcr_module

from django.conf import settings

from spotifywrapper import Auth


vcr = vcr_module.VCR(filter_headers=['Authorization'])
cassettes_path = os.path.join(settings.BASE_DIR,
                              'spotifywrapper/tests/vcr_cassettes/{}')


class TestAuthInit:

    @pytest.fixture(autouse=True)
    def initial(self):
        client_id = settings.SPOTIFY_CLIENT_ID
        client_secret = settings.SPOTIFY_CLIENT_SECRET

        self.expected_auth_key = base64.b64encode(
            f'{client_id}:{client_secret}'.encode('ascii')).decode('ascii')
        self.expected_url = 'https://accounts.spotify.com/api/token'

    def test_initialize_auth_object_with_code(self):
        spfy_auth = Auth()

        assert settings.SPOTIFY_REDIRECT_URI == spfy_auth.redirect_uri
        assert self.expected_auth_key == spfy_auth.auth_key
        assert self.expected_url == spfy_auth.url


class TestAuthMethods:

    def test_headers_property(self):
        spfy_auth = Auth()

        fake_auth_key = 'fake_key'
        spfy_auth.auth_key = fake_auth_key

        headers = spfy_auth._headers
        assert isinstance(headers, dict)
        assert 'application/x-www-form-urlencoded' == headers['Content-Type']
        assert f'Basic {fake_auth_key}' == headers['Authorization']

    @vcr.use_cassette(cassettes_path.format('auth_request_tokens.yml'))
    def test_request_tokens(self):
        code = 'AQDQ943dAEguAxMypx0JuexLtM0Z7egb2hI-dpo5s-kQBAAn83yHS57nXJlT0kBFEs7o1YcjMdWCGrWBYFEP138tfRzRHBMI9aEDXhb08HxyUoc3SuHsu-WZvUJzAf57rKiUIt-XUL8fCsqYNJTaQMQG6E7t4BsOwtPyj_keLoIv8n6vpsRsseA4rhtxMkWyEP-cynmDBUI98JOTvDM7r43SaxpPBvWHXDpYvJzyJbRVKYa70SHfIg'  # NOQA
        spfy_auth = Auth()

        requests_to_mock_path = 'spotifywrapper.auth.requests.post'
        with patch(requests_to_mock_path, wraps=requests.post) as mock_post:
            access_token, refresh_token = spfy_auth.request_tokens(code)

        expected_call = call(
            spfy_auth.url,
            data={
                'grant_type': 'authorization_code',
                'code': code,
                'redirect_uri': spfy_auth.redirect_uri,
            },
            headers=spfy_auth._headers,
        )

        assert expected_call in mock_post.call_args_list
        assert access_token
        assert refresh_token

    @vcr.use_cassette(cassettes_path.format('auth_refresh_token.yml'))
    def test_refresh_access_token(self):
        refresh_token = 'AQB9Ft0eD6E-aB4IxK5d-OPuDhwYfcXvDhBI1sCid8PO2spKVTmhZgrRbC6C6jWmDCW3_rXZxyRPmFuEzk9g7fyi7GGqHobKIUwWzrL-W5f-MMRfpYHl0dF1yVUiYK8qJaM' # NOQA
        spfy_auth = Auth()

        requests_to_mock_path = 'spotifywrapper.auth.requests.post'
        with patch(requests_to_mock_path, wraps=requests.post) as mock_post:
            access_token = spfy_auth.refresh_access_token(refresh_token)

        expected_call = call(
            spfy_auth.url,
            data={
                'grant_type': 'refresh_token',
                'refresh_token': refresh_token,
            },
            headers=spfy_auth._headers,
        )

        assert expected_call in mock_post.call_args_list
        assert access_token
