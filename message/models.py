from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from shared.conversion import datetime_to_json
from stream.models import Stream


class Message(models.Model):
    user = models.ForeignKey(User, blank=True, null=True)
    username = models.CharField(max_length=64, blank=True, null=True)
    stream = models.ForeignKey(Stream)
    content = models.TextField()
    sent_at = models.DateTimeField(default=timezone.now(), blank=True)

    def dump(self):
        return {
            'user': getattr(self.user, 'id', None),
            'username': self.username,
            'stream': getattr(self.stream, 'id', None),
            'content': self.content,
            'sent_at': datetime_to_json(self.sent_at)
        }
