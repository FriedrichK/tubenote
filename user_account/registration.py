from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from django.contrib.auth.hashers import check_password

from rest_framework.authtoken.models import Token

from user_account.exceptions import UsernameAlreadyExistsException


def register_user(username, email, password):
    try:
        with transaction.atomic():
            user = User.objects.create_user(username, email, password)
            return Token.objects.create(user=user)
    except IntegrityError:
        return return_token_for_existing_user(username, password)


def return_token_for_existing_user(username, password):
    user = User.objects.get(username=username)
    if not check_password(password, user.password):
        raise UsernameAlreadyExistsException('A user with the username %s already exists and passwords do not match' % username)

    return get_or_create_token_for_user(user)


def get_or_create_token_for_user(user):
    result = Token.objects.filter(user=user).order_by('-created')
    if isinstance(result, Token):
        return result
    if result is None or len(result) < 1:
        return Token.objects.create(user=user)
    return result[0]
