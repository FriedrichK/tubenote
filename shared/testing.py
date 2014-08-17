from django.contrib.auth.models import User

from user_account.models import AnonymousButNamedUser
from stream.models import Stream

EMPTY_USER = None
GENERIC_MOCK_RESULT = 'we can put this when it does not matter what the result really is'

TEST_USER_NAME = "test_user"
TEST_USER_EMAIL = "test@user.com"
TEST_USER_PASSWORD = "test_password"
TEST_USER_INCORRECT_PASSWORD = 'not_the_test_password'

TEST_RESPONSE_CONTENT = "this content is what we expected"

TEST_TOKEN = "test_token"

TEST_MESSAGE_CONTENT = "this is the message content we expected"

TEST_STREAM_IDENTIFIER = "this is a test stream with spaces, Capitals & $pecial ch@racters"


def create_mock_stream(user, stream_identifier):
    content = {'identifier': stream_identifier}
    if isinstance(user, User):
        content['created_by_user'] = user
    if isinstance(user, AnonymousButNamedUser):
        content['created_by_username'] = AnonymousButNamedUser.username
    stream = Stream(**content)
    stream.save()
    return stream
