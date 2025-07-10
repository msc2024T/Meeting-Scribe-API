from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserQuota
from datetime import date
from .services import UserQuotaService


@receiver(post_save, sender=User)
def create_user_quota(sender, instance, created, **kwargs):
    if created:
        service = UserQuotaService(instance)
        service.create_quota(max_minutes=60)
