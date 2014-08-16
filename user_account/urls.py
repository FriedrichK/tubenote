from django.conf.urls import patterns, url

from user_account.views import AccountView

urlpatterns = patterns(
    '',
    url(r'^$', AccountView.as_view(), name='account'),
)
