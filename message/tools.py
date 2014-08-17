from user_account.models import AnonymousButNamedUser
from user_account.authentication import user_is_enabled
from user_account.exceptions import UserIsNotEnabledException
from message.models import Message


def create_message(user, stream, content):
    if isinstance(user, AnonymousButNamedUser):
        return create_message_for_anonymous_but_named_user(user, stream, content)

    if not user_is_enabled(user):
        raise UserIsNotEnabledException

    message = Message(user=user, stream=stream, content=content)
    message.save()
    return message


def create_message_for_anonymous_but_named_user(user, stream, content):
    message = Message(username=user.username, stream=stream, content=content)
    message.save()
    return message
