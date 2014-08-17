from django.contrib.auth.models import User

from user_account.models import AnonymousButNamedUser


def user_is_registered(user_variable):
    if isinstance(user_variable, User):
        return True
    return False


def user_is_anonymous_but_named(user_variable):
    if isinstance(user_variable, AnonymousButNamedUser):
        return True
    return False


def user_variable_is_valid(user_variable):
    if not user_is_registered(user_variable) and not user_is_anonymous_but_named(user_variable):
        return False
    return True
