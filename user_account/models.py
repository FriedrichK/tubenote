from django.contrib.auth.models import AnonymousUser


class AnonymousButNamedUser(AnonymousUser):

    @classmethod
    def create_user(self, name):
        return AnonymousButNamedUser(name)

    def __init__(self, username):
        self.username = username

    def is_authenticated(self):
        return True
