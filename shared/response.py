import json

from django.http import HttpResponseBadRequest


class RestHttpResponseBadRequest(HttpResponseBadRequest):
    def __init__(self, content=b'', *args, **kwargs):
        super(RestHttpResponseBadRequest, self).__init__(*args, **kwargs)
        self.content = json.dumps({'success': False, 'message': content})
