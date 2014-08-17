from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

from shared.conversion import datetime_to_json


class Stream(models.Model):
    created_by_user = models.ForeignKey(User, blank=True, null=True)
    created_by_username = models.CharField(max_length=64, blank=True, null=True)
    identifier = models.CharField(max_length=64, unique=True)
    created_at = models.DateTimeField(default=timezone.now())

    def dump(self):
        return {
            'created_by_user': getattr(self.created_by_user, 'id', None),
            'created_by_username': self.created_by_username,
            'identifier': self.identifier,
            'created_at': datetime_to_json(self.created_at)
        }
