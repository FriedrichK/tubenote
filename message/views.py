from shared.response import RestHttpResponse, RestHttpResponseBadRequest

from rest_framework.views import APIView

from shared.tools import request_has_required_parameters
from user_account.exceptions import UserIsNotEnabledException
from stream.tools import get_stream_by_identifier
from message.tools import create_message


class MessageView(APIView):

    def post(self, request, format=None):
        success, missing_parameters = request_has_required_parameters(request, ['stream_identfier', 'content'], 'POST')
        if not success:
            return RestHttpResponseBadRequest('request missed mandatory parameter(s): %s' % ', '.join(missing_parameters))

        content = request.POST.get('content')
        if content is None or content == '':
            return RestHttpResponseBadRequest('message content cannot be empty')

        stream = get_stream_by_identifier(request.POST.get('stream_identfier', None))
        if stream is None:
            return RestHttpResponseBadRequest('the stream this message is supposed to be posted to does not exist')

        try:
            message = create_message(request.user, stream, content)
        except UserIsNotEnabledException:
            return RestHttpResponseBadRequest('unauthorized')

        return RestHttpResponse(message.dump())
