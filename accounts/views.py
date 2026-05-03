import requests
from django.conf import settings
from django.contrib.auth import login
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils import timezone
from datetime import timedelta

from .models import SpotifyUser


def spotify_login(request):
    params = {
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'response_type': 'code',
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
        'scope': 'playlist-modify-public playlist-modify-private',
    }
    auth_url = requests.Request('GET', 'https://accounts.spotify.com/authorize', params=params).prepare().url
    return redirect(auth_url)


def spotify_callback(request):
    code = request.GET.get('code')

    token_response = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': settings.SPOTIFY_REDIRECT_URI,
        'client_id': settings.SPOTIFY_CLIENT_ID,
        'client_secret': settings.SPOTIFY_CLIENT_SECRET,
    })
    token_data = token_response.json()

    access_token = token_data['access_token']
    refresh_token = token_data['refresh_token']
    expires_in = token_data['expires_in']
    token_expiry = timezone.now() + timedelta(seconds=expires_in)

    profile_response = requests.get('https://api.spotify.com/v1/me', headers={
        'Authorization': f'Bearer {access_token}'
    })
    profile = profile_response.json()
    spotify_user_id = profile['id']

    user, _ = User.objects.get_or_create(username=spotify_user_id)
    spotify_user, _ = SpotifyUser.objects.update_or_create(
        user=user,
        defaults={
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_expiry': token_expiry,
            'spotify_user_id': spotify_user_id,
        }
    )

    login(request, user)
    return redirect('/')