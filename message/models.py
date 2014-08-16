from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Message(models.Model):
    user = models.ForeignKey(User)
    content = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now(), blank=True)
