from django.test import TestCase
from django.contrib.auth.models import User

from shared.testing import TEST_USER_NAME, TEST_USER_EMAIL, TEST_USER_PASSWORD, TEST_MESSAGE_CONTENT
from user_account.models import AnonymousButNamedUser
from user_account.exceptions import UserIsNotEnabledException
from message.tools import create_message


class MessageTestCase(TestCase):

    def test_creates_message_as_expected(self):
        user = User.objects.create_user(TEST_USER_NAME, TEST_USER_EMAIL, TEST_USER_PASSWORD)
        message = create_message(user, TEST_MESSAGE_CONTENT)
        self.assertEqual(message.id, 1)

    def test_throws_expected_exception_when_user_is_not_enabled(self):
        user = User(username=TEST_USER_NAME, email=TEST_USER_EMAIL, is_active=False)
        user.save()
        self.assertRaises(UserIsNotEnabledException, create_message, user, TEST_MESSAGE_CONTENT)

    def test_creates_message_as_expected_when_user_is_anonymous_except_for_username(self):
        user = AnonymousButNamedUser.create_user(TEST_USER_NAME)
        message = create_message(user, TEST_MESSAGE_CONTENT)
        self.assertEqual(message.username, TEST_USER_NAME)

    def test_returns_expected_message_dump(self):
        user = User.objects.create_user(TEST_USER_NAME, TEST_USER_EMAIL, TEST_USER_PASSWORD)

        message = create_message(user, TEST_MESSAGE_CONTENT)
        actual = message.dump()

        self.assertEqual(actual['user'], 1)
        self.assertEqual(actual['content'], TEST_MESSAGE_CONTENT)
        self.assertEqual(actual['username'], None)
        self.assertTrue('sent_at' in actual)

    def test_returns_expected_message_dump_when_user_is_anonymous_except_for_username(self):
        user = AnonymousButNamedUser.create_user(TEST_USER_NAME)

        message = create_message(user, TEST_MESSAGE_CONTENT)
        actual = message.dump()

        self.assertEqual(actual['user'], None)
        self.assertEqual(actual['content'], TEST_MESSAGE_CONTENT)
        self.assertEqual(actual['username'], TEST_USER_NAME)
        self.assertTrue('sent_at' in actual)
