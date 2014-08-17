from user_account.exceptions import InvalidUserException, UserIsNotEnabledException
from user_account.tools import user_is_anonymous_but_named, user_variable_is_valid, user_is_registered
from user_account.authentication import user_is_enabled
from stream.models import Stream
from stream.exceptions import InvalidStreamIdentfierException


def create_or_return_stream(user, stream_identifier):
    stream = get_stream_by_identifier(stream_identifier)
    if not stream is None:
        return stream
    return create_stream(stream_identifier)


def get_stream_by_identifier(stream_identifier):
    try:
        return Stream.objects.get(identifier=stream_identifier)
    except Stream.DoesNotExist:
        return None


def create_stream(user, stream_identifier):
    if not user_variable_is_valid(user):
        raise InvalidUserException()

    if not stream_identifier_is_valid(stream_identifier):
        raise InvalidStreamIdentfierException()

    if user_is_registered(user) and not user_is_enabled(user):
        raise UserIsNotEnabledException()

    data = {'identifier': stream_identifier}
    if user_is_anonymous_but_named(user):
        data['created_by_username'] = user.username
    else:
        data['created_by_user'] = user

    stream = Stream(**data)
    stream.save()

    return stream


def stream_identifier_is_valid(stream_identifier):
    if not isinstance(stream_identifier, str) and not isinstance(stream_identifier, unicode):
        return False
    if stream_identifier == '':
        return False
    return True
