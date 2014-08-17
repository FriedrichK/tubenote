from django.conf.urls import patterns, url

from stream.views import StreamView

urlpatterns = patterns(
    '',
    url(r'^$', StreamView.as_view(), name='stream'),
)
