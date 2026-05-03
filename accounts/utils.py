import requests
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


def get_valid_token(spotify_user):
    if timezone.now() >= spotify_user.token_expiry:
        response = requests.post('https://accounts.spotify.com/api/token', data={
            'grant_type': 'refresh_token',
            'refresh_token': spotify_user.refresh_token,
            'client_id': settings.SPOTIFY_CLIENT_ID,
            'client_secret': settings.SPOTIFY_CLIENT_SECRET,
        })
        token_data = response.json()
        spotify_user.access_token = token_data['access_token']
        spotify_user.token_expiry = timezone.now() + timedelta(seconds=token_data['expires_in'])
        spotify_user.save()

    return spotify_user.access_token