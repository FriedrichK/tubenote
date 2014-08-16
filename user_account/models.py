from django.contrib.auth.models import AnonymousUser


class AnonymousButNamedUser(AnonymousUser):
    def __init__(self, username):
        self.username = username

    def is_authenticated(self):
        return True
