import json

from mock import patch

from django.test import TestCase
from django.contrib.auth.models import User

from rest_framework.test import APIClient

from shared.testing import GENERIC_MOCK_RESULT, EMPTY_USER, TEST_USER_NAME
from user_account.models import AnonymousButNamedUser
from user_account.exceptions import InvalidUserException, UserIsNotEnabledException
from stream.models import Stream
from stream.tools import create_or_return_stream, create_stream, get_stream_by_identifier


MOCK_STREAM_IDENTIFIER = 'this_is_a_mock_stream_identifier'
MOCK_STREAM_IDENTIFIER_THAT_DOES_NOT_EXIST = 'this does not exist'


class StreamTestCase(TestCase):

    @patch('stream.tools.create_stream')
    @patch('stream.tools.get_stream_by_identifier')
    def test_returns_stream_if_stream_exists(self, get_stream_by_identifier_mock, create_stream_mock):
        get_stream_by_identifier_mock.return_value = "something that is not None"

        create_or_return_stream(EMPTY_USER, MOCK_STREAM_IDENTIFIER)

        self.assertTrue(get_stream_by_identifier_mock.called)
        self.assertFalse(create_stream_mock.called)

    @patch('stream.tools.create_stream')
    @patch('stream.tools.get_stream_by_identifier')
    def test_triggers_stream_creation_if_stream_does_not_exist(self, get_stream_by_identifier_mock, create_stream_mock):
        get_stream_by_identifier_mock.return_value = None
        create_stream_mock.return_value = GENERIC_MOCK_RESULT

        actual = create_or_return_stream(EMPTY_USER, MOCK_STREAM_IDENTIFIER)

        self.assertTrue(get_stream_by_identifier_mock.called)
        self.assertTrue(create_stream_mock.called)
        self.assertEquals(actual, GENERIC_MOCK_RESULT)

    def test_creates_stream_as_expected(self):
        user = User(username=TEST_USER_NAME)
        user.save()

        actual = create_stream(user, MOCK_STREAM_IDENTIFIER)

        self.assertEquals(actual.created_by_user.username, TEST_USER_NAME)
        self.assertEquals(actual.identifier, MOCK_STREAM_IDENTIFIER)

    def test_fails_to_create_stream_when_user_is_none(self):
        self.assertRaises(InvalidUserException, create_stream, None, MOCK_STREAM_IDENTIFIER)

    def test_fails_to_create_stream_when_user_is_not_enabled(self):
        user = User(username=TEST_USER_NAME, is_active=False)
        user.save()

        self.assertRaises(UserIsNotEnabledException, create_stream, user, MOCK_STREAM_IDENTIFIER)

    def test_creates_stream_as_expected_when_user_is_anonymous_but_named(self):
        user = AnonymousButNamedUser(username=TEST_USER_NAME)

        actual = create_stream(user, MOCK_STREAM_IDENTIFIER)

        self.assertEquals(actual.created_by_username, TEST_USER_NAME)
        self.assertEquals(actual.identifier, MOCK_STREAM_IDENTIFIER)

    def test_returns_expected_streamm_by_identifier(self):
        stream = Stream(identifier=MOCK_STREAM_IDENTIFIER)
        stream.save()

        actual = get_stream_by_identifier(MOCK_STREAM_IDENTIFIER)

        self.assertEqual(actual.identifier, MOCK_STREAM_IDENTIFIER)

    def test_throws_expected_exception_if_stream_does_not_exist(self):
        self.assertIsNone(get_stream_by_identifier(MOCK_STREAM_IDENTIFIER_THAT_DOES_NOT_EXIST))

    def test_returns_expected_stream_dump(self):
        user = User(username=TEST_USER_NAME)
        user.save()

        result = create_stream(user, MOCK_STREAM_IDENTIFIER)
        actual = result.dump()

        self.assertEqual(actual['identifier'], MOCK_STREAM_IDENTIFIER)
        self.assertEqual(actual['created_by_user'], user.id)
        self.assertIsNone(actual['created_by_username'])

    def test_returns_expected_stream_dump_when_user_is_anonymous_but_named(self):
        user = AnonymousButNamedUser(username=TEST_USER_NAME)

        result = create_stream(user, MOCK_STREAM_IDENTIFIER)
        actual = result.dump()

        self.assertEqual(actual['identifier'], MOCK_STREAM_IDENTIFIER)
        self.assertEqual(actual['created_by_username'], TEST_USER_NAME)
        self.assertIsNone(actual['created_by_user'])


class StreamViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()

    @patch('stream.views.create_or_return_stream')
    def test_triggers_stream_creation_as_expected(self, create_or_return_stream_mock):
        create_or_return_stream_mock.return_value = MockStream()

        user = User(username=TEST_USER_NAME)
        user.save()
        stream = Stream(created_by_user=user, identifier=MOCK_STREAM_IDENTIFIER)
        stream.save()

        self.client.force_authenticate(user=user)

        response = self.client.post('/api/stream/', {'stream_identifier': MOCK_STREAM_IDENTIFIER})
        actual = json.loads(response.content)

        self.assertEquals(actual['data']['mock'], True)
        self.client.force_authenticate(user=None)

    def test_stream_creation_view_fails_if_parameters_are_missing(self):
        user = User(username=TEST_USER_NAME)
        user.save()

        self.client.force_authenticate(user=user)

        response = self.client.post('/api/stream/', {'not_putting_any_required_parameter': True})

        self.assertEquals(response.status_code, 400)

        self.client.force_authenticate(user=None)

    def test_stream_creation_view_fails_if_the_user_is_invalid(self):
        pass

    def test_stream_creation_view_fails_if_the_stream_identifier_is_invalid(self):
        user = User(username=TEST_USER_NAME)
        user.save()

        self.client.force_authenticate(user=user)

        response = self.client.post('/api/stream/', {'stream_idetnifier': ''})

        self.assertEquals(response.status_code, 400)

        self.client.force_authenticate(user=None)

    @patch('stream.views.create_or_return_stream')
    def test_stream_creation_view_fails_if_the_user_is_not_enabled(self, create_or_return_stream_mock):
        create_or_return_stream_mock.side_effect = UserIsNotEnabledException()

        user = User(username=TEST_USER_NAME, is_active=False)
        user.save()
        stream = Stream(created_by_user=user, identifier=MOCK_STREAM_IDENTIFIER)
        stream.save()

        self.client.force_authenticate(user=user)

        response = self.client.post('/api/stream/', {'stream_identifier': MOCK_STREAM_IDENTIFIER})

        self.assertEquals(response.status_code, 400)

        self.client.force_authenticate(user=None)

    @patch('stream.views.get_stream_by_identifier')
    def test_gets_stream_dump_as_expected(self, get_stream_by_identifier_mock):
        user = User(username=TEST_USER_NAME, is_active=False)
        stream = Stream(created_by_user=user, identifier=MOCK_STREAM_IDENTIFIER)
        get_stream_by_identifier_mock.return_value = stream

        response = self.client.get('/api/stream/', {'stream_identifier': MOCK_STREAM_IDENTIFIER})
        actual = json.loads(response.content)

        self.assertEqual(actual['data']['identifier'], MOCK_STREAM_IDENTIFIER)

    def test_stream_retrieval_view_fails_if_paramateres_are_missing(self):
        response = self.client.get('/api/stream/', {'not_putting_any_required_parameter': True})
        self.assertEqual(response.status_code, 400)

    def test_stream_retrieval_view_fails_if_stream_identifier_is_invalid(self):
        response = self.client.get('/api/stream/', {'stream_identifier': ''})
        self.assertEqual(response.status_code, 400)

    def test_stream_retrieval_view_fails_if_stream_cannot_be_found(self):
        response = self.client.get('/api/stream/', {'stream_identifier': MOCK_STREAM_IDENTIFIER_THAT_DOES_NOT_EXIST})
        print response
        self.assertEqual(response.status_code, 404)


class MockStream(object):
    def dump(self):
        return {'mock': True}
