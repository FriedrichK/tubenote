from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from shared.conversion import datetime_to_json


class Message(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    username = models.CharField(max_length=64, blank=True, null=True)
    content = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now(), blank=True)

    def dump(self):
        return {
            'user': getattr(self.user, 'id', None),
            'username': self.username,
            'content': self.content,
            'sent_at': datetime_to_json(self.sent_at)
        }
