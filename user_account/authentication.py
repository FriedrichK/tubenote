from rest_framework import authentication

from user_account.models import AnonymousButNamedUser

METHODS = ['GET', 'POST', 'UPDATE', 'DELETE']


class UserNameAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        user = None
        for method in METHODS:
            if hasattr(request, method):
                check = getattr(request, method).get('user', False)
                if check:
                    user = check

        if not user is None:
            return (AnonymousButNamedUser(user), None)

        return None
