from django.test import TestCase
from django.http import HttpResponse
from django.contrib.auth.models import User

from rest_framework.test import APIRequestFactory
from rest_framework.test import APIClient
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework.authtoken.models import Token

TEST_USER_NAME = "test_user"
TEST_USER_EMAIL = "test@user.com"
TEST_USER_PASSWORD = "test_password"
TEST_RESPONSE_CONTENT = "this content is what we expected"


class MessageTestCase(TestCase):

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
