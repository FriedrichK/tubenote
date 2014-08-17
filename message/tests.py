import json

from mock import patch

from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIClient

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


class MessageViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    @patch('message.views.create_message')
    def test_message_create_view_calls_create_message(self, create_message_mock):
        create_message_mock.return_value = MockMessage()
        user = User.objects.create_user(TEST_USER_NAME, TEST_USER_EMAIL, TEST_USER_PASSWORD)
        self.client.force_authenticate(user=user)
        message_data = {
            'content': TEST_MESSAGE_CONTENT
        }

        response = self.client.post('/api/message/', message_data)
        actual = json.loads(response.content)

        self.assertEquals(actual, {'message': None, 'data': {'mock': True}, 'success': True})

        self.client.force_authenticate(user=None)

    def test_message_create_view_fails_because_user_is_unauthenticated(self):
        response = self.client.post('/api/message/', {})
        self.assertEqual(response.status_code, 401)

    def test_message_create_view_fails_because_user_is_not_enabled(self):
        user = User(username=TEST_USER_NAME, email=TEST_USER_EMAIL, is_active=False)
        user.save()
        self.client.force_authenticate(user=user)

        response = self.client.post('/api/message/', {'content': 'xxx'})
        print response

        self.assertEqual(response.status_code, 400)

        self.client.force_authenticate(user=None)

    def test_message_create_view_fails_because_request_parameter_is_missing(self):
        user = User.objects.create_user(TEST_USER_NAME, TEST_USER_EMAIL, TEST_USER_PASSWORD)
        self.client.force_authenticate(user=user)

        response = self.client.post('/api/message/', {})

        self.assertEquals(response.status_code, 400)

        self.client.force_authenticate(user=None)

    def test_message_create_view_fails_because_message_content_is_empty(self):
        user = User.objects.create_user(TEST_USER_NAME, TEST_USER_EMAIL, TEST_USER_PASSWORD)
        self.client.force_authenticate(user=user)

        response = self.client.post('/api/message/', {'content': ''})

        self.assertEquals(response.status_code, 400)

        self.client.force_authenticate(user=None)


class MockMessage():
    def dump(self):
        return {'mock': True}
