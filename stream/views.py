from shared.response import RestHttpResponse, RestHttpResponseBadRequest, RestHttpResponseNotFound

from rest_framework.views import APIView

from user_account.exceptions import InvalidUserException, UserIsNotEnabledException
from shared.tools import request_has_required_parameters
from stream.tools import create_or_return_stream, get_stream_by_identifier, stream_identifier_is_valid
from stream.exceptions import InvalidStreamIdentfierException


class StreamView(APIView):

    def post(self, request, format=None):
        success, missing_parameters = request_has_required_parameters(request, ['stream_identifier'], 'POST')
        if not success:
            return RestHttpResponseBadRequest('request missed mandatory parameter(s): %s' % ', '.join(missing_parameters))

        stream_identifier = request.POST.get('stream_identifier')
        if not stream_identifier_is_valid(stream_identifier):
            return RestHttpResponseBadRequest('invalid stream identifier')

        try:
            stream = create_or_return_stream(request.user, stream_identifier)
            return RestHttpResponse(stream.dump())
        except InvalidUserException:
            return RestHttpResponseBadRequest('invalid user')
        except InvalidStreamIdentfierException:
            return RestHttpResponseBadRequest('invalid stream identifier')
        except UserIsNotEnabledException:
            return RestHttpResponseBadRequest('user is not enabled')

    def get(self, request, format=None):
        success, missing_parameters = request_has_required_parameters(request, ['stream_identifier'], 'GET')
        if not success:
            return RestHttpResponseBadRequest('request missed mandatory parameter(s): %s' % ', '.join(missing_parameters))

        stream_identifier = request.GET.get('stream_identifier')
        if not stream_identifier_is_valid(stream_identifier):
            return RestHttpResponseBadRequest('stream identifier cannot be empty')

        stream = get_stream_by_identifier(stream_identifier)
        if stream is None:
            return RestHttpResponseNotFound('stream for stream ID %s could not be found' % stream_identifier)

        return RestHttpResponse(stream.dump())
