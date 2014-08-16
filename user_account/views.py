from shared.response import RestHttpResponseBadRequest

from rest_framework.views import APIView
from rest_framework.response import Response

from user_account.registration import register_user


class AccountView(APIView):
    def post(self, request, format=None):
        data = {}
        required = ['username', 'email', 'password']
        for r in required:
            item = request.POST.get(r, False)
            if item is False:
                return RestHttpResponseBadRequest('parameter %s is missing' % item)
            else:
                data[r] = item

        token = register_user(data['username'], data['email'], data['password'])

        return Response({'success': True, 'token': token.key})
