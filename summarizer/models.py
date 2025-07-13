from django.db import models
from transcription.models import Transcription


class Summary(models.Model):
    transcription = models.OneToOneField(
        Transcription, on_delete=models.CASCADE)
    subject = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Summary for {self.transcription.audio_file.name} "


class actionItem(models.Model):
    summary = models.ForeignKey(
        Summary, on_delete=models.CASCADE, related_name='action_items')
    description = models.TextField()
    assigned_to = models.CharField(max_length=255, blank=True, null=True)
    due_date = models.CharField(blank=True, null=True)
    status = models.CharField(max_length=50, default='pending')

    def __str__(self):
        return f"Action Item: {self.description[:50]} for {self.summary.transcription.audio_file.name}"


class KeyPoint(models.Model):
    summary = models.ForeignKey(
        Summary, on_delete=models.CASCADE, related_name='key_points')
    content = models.TextField()

    def __str__(self):
        return f"Key Point: {self.content[:50]}"
