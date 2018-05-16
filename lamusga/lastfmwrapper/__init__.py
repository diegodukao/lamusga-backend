import requests
from django.conf import settings

session = requests.Session()
session.params = {}
session.params['api_key'] = settings.LASTFM_API_KEY
session.params['format'] = 'json'


from .user import User  # NOQA
