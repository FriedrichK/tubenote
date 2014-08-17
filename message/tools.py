from user_account.models import AnonymousButNamedUser
from user_account.authentication import user_is_enabled
from user_account.exceptions import UserIsNotEnabledException
from message.models import Message


def create_message(user, content):
    if isinstance(user, AnonymousButNamedUser):
        return create_message_for_anonymous_but_named_user(user, content)

    if not user_is_enabled(user):
        raise UserIsNotEnabledException

    message = Message(user=user, content=content)
    message.save()
    return message


def create_message_for_anonymous_but_named_user(user, content):
    message = Message(username=user.username, content=content)
    message.save()
    return message
