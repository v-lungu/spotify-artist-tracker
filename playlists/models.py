from django.db import models
from accounts.models import SpotifyUser


class TrackedArtist(models.Model):
    user = models.ForeignKey(SpotifyUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)


class PlaylistRun(models.Model):
    user = models.ForeignKey(SpotifyUser, on_delete=models.CASCADE)
    last_run = models.DateField()
    playlist_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)