import json

from django.http import HttpResponseBadRequest

from rest_framework.response import Response


class RestHttpResponse(Response):
    def __init__(self, data=None, status=200,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        data = {'success': True, 'message': None, 'data': data}
        super(RestHttpResponse, self).__init__(data=data, status=status, template_name=template_name, headers=headers, exception=exception, content_type=content_type)


class RestHttpResponseBadRequest(HttpResponseBadRequest):
    def __init__(self, content=b'', *args, **kwargs):
        super(RestHttpResponseBadRequest, self).__init__(*args, **kwargs)
        self.content = json.dumps({'success': False, 'data': None, 'message': content})
