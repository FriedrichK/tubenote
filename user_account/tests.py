import json

from mock import patch

from django.test import TestCase
from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.authtoken.models import Token

from user_account.registration import register_user
from user_account.exceptions import UsernameAlreadyExistsException

TEST_USER_NAME = "test_user"
TEST_USER_EMAIL = "test@user.com"
TEST_USER_PASSWORD = "test_password"
TEST_USER_INCORRECT_PASSWORD = 'not_the_test_password'
TEST_RESPONSE_CONTENT = "this content is what we expected"
TEST_TOKEN = "test_token"


class RegistrationTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def test_returns_token_on_user_registration(self):
        token = register_user(TEST_USER_NAME, TEST_USER_EMAIL, TEST_USER_PASSWORD)
        self.assertIsInstance(token, Token)

    def test_returns_existing_token_if_username_and_password_match_existing_user(self):
        user = User.objects.create_user(TEST_USER_NAME, TEST_USER_EMAIL, TEST_USER_PASSWORD)
        token = Token.objects.create(user=user)
        actual = register_user(TEST_USER_NAME, TEST_USER_EMAIL, TEST_USER_PASSWORD)
        self.assertEqual(actual.key, token.key)

    def test_generates_new_token_if_username_and_password_match_existing_user_but_no_token_exists_yet(self):
        User.objects.create_user(TEST_USER_NAME, TEST_USER_EMAIL, TEST_USER_PASSWORD)
        register_user(TEST_USER_NAME, TEST_USER_EMAIL, TEST_USER_PASSWORD)

    def test_raises_appropriate_exception_if_username_already_exists_but_password_does_not_match(self):
        User.objects.create_user(TEST_USER_NAME, TEST_USER_EMAIL, TEST_USER_PASSWORD)
        self.assertRaises(UsernameAlreadyExistsException, register_user, TEST_USER_NAME, TEST_USER_EMAIL, TEST_USER_INCORRECT_PASSWORD)

    @patch('user_account.views.register_user')
    def test_registration_view_returns_token_as_expected(self, register_user_mock):
        register_user_mock.return_value = MockToken(TEST_TOKEN)

        response = self.client.post('/api/account/', {'username': TEST_USER_NAME, 'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD})
        self.assertEqual(json.loads(response.content)['token'], TEST_TOKEN)

    def test_registration_view_returns_error_if_no_information_is_given(self):
        response = self.client.post('/api/account/', {'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD})
        self.assertEqual(response.status_code, 400)

    def test_registration_view_returns_error_if_username_is_missing(self):
        response = self.client.post('/api/account/', {'email': TEST_USER_EMAIL, 'password': TEST_USER_PASSWORD})
        self.assertEqual(response.status_code, 400)

    def test_registration_view_returns_error_if_email_is_missing(self):
        response = self.client.post('/api/account/', {'username': TEST_USER_NAME, 'password': TEST_USER_PASSWORD})
        self.assertEqual(response.status_code, 400)

    def test_registration_view_returns_error_if_password_is_missing(self):
        response = self.client.post('/api/account/', {'username': TEST_USER_NAME, 'email': TEST_USER_EMAIL})
        self.assertEqual(response.status_code, 400)


class AuthenticationTestCase(TestCase):

    def setUp(self):
        self.factory = APIRequestFactory()
        self.client = APIClient()

    def test_should_generate_successful_view_response_if_token_is_provided(self):
        test_user = User.objects.create_user(TEST_USER_NAME, TEST_USER_EMAIL, TEST_USER_PASSWORD)
        token = Token.objects.create(user=test_user)

        request = self.factory.post('/api/message', {}, **{'HTTP_AUTHORIZATION': 'Token ' + token.key})
        response = RequestTestView.as_view()(request)

        self.assertEqual(response.content, TEST_RESPONSE_CONTENT)

    def test_should_generate_successful_view_repsonse_if_username_is_provided(self):
        request = self.factory.post('/api/message/', {'user': TEST_USER_NAME})
        response = RequestTestView.as_view()(request)
        self.assertEqual(response.content, TEST_RESPONSE_CONTENT)

    def test_should_generate_unauthorized_401_response_if_no_authentication(self):
        request = self.factory.post('/api/message/', {})
        response = RequestTestView.as_view()(request)
        self.assertEqual(response.status_code, 401)


class RequestTestView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        return HttpResponse(TEST_RESPONSE_CONTENT)


class MockToken(object):
    def __init__(self, token):
        self.key = token
