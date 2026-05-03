from django.db import models
from django.contrib.auth.models import User


class SpotifyUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    access_token = models.TextField()
    refresh_token = models.TextField()
    token_expiry = models.DateTimeField()
    spotify_user_id = models.CharField(max_length=100)
