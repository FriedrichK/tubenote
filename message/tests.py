from django.test import TestCase
from django.contrib.auth.models import User

from shared.testing import TEST_USER_NAME, TEST_USER_EMAIL, TEST_USER_PASSWORD, TEST_MESSAGE_CONTENT
from user_account.models import AnonymousButNamedUser
from message.tools import create_message


class MessageTestCase(TestCase):

    def test_creates_message_as_expected(self):
        user = User.objects.create_user(TEST_USER_NAME, TEST_USER_EMAIL, TEST_USER_PASSWORD)
        message = create_message(user, TEST_MESSAGE_CONTENT)
        self.assertEqual(message.id, 1)

    def test_creates_message_as_expected_when_user_is_anonymous_except_for_username(self):
        user = AnonymousButNamedUser.create_user(TEST_USER_NAME)
        message = create_message(user, TEST_MESSAGE_CONTENT)
        self.assertEqual(message.username, TEST_USER_NAME)
