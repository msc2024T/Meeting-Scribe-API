from django.db import models


class Transcription(models.Model):
    audio_file = models.ForeignKey(
        'files.AudioFile', on_delete=models.CASCADE, related_name='transcriptions')
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Transcription for {self.audio_file.name} at {self.created_at}"
