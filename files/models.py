from django.db import models
from django.contrib.auth.models import User as AuthUser


class AudioFile(models.Model):

    id = models.CharField(max_length=255, primary_key=True,
                          help_text="Unique identifier for the audio file")
    name = models.CharField(max_length=255, help_text="Name of the audio file")
    size = models.PositiveIntegerField(
        help_text="Size of the audio file in bytes")
    extention = models.CharField(
        max_length=10, help_text="File extension (e.g., mp3, wav)")
    durtion_seconds = models.PositiveIntegerField(
        help_text="Duration of the audio file in seconds")

    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)

    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.file.name}"

    class Meta:
        verbose_name = "Audio File"
        verbose_name_plural = "Audio Files"
        ordering = ['-uploaded_at']
