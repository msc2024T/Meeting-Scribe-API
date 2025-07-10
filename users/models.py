from django.db import models
from django.contrib.auth.models import User as AuthUser


class UserQuota(models.Model):

    user = models.OneToOneField(
        AuthUser, on_delete=models.CASCADE, related_name='quota')
    max_minutes = models.PositiveIntegerField(
        default=60, help_text="Maximum minutes of audio per month")
    used_minutes = models.PositiveIntegerField(
        default=0, help_text="Used minutes of audio this month")
    reset_date = models.DateField(
        auto_now_add=True, help_text="Date when the quota resets")
    created_at = models.DateTimeField(
        auto_now_add=True, help_text="When the quota was created")

    def __str__(self):
        return f"{self.user.username} - Quota: {self.used_minutes}/{self.max_minutes} minutes"
