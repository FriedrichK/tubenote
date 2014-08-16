from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token


def register_user(username, email, password):
    user = User.objects.create_user(username, email, password)
    return Token.objects.create(user=user)
