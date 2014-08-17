from django.conf.urls import patterns, url

from message.views import MessageView

urlpatterns = patterns(
    '',
    url(r'^$', MessageView.as_view(), name='message'),
)
