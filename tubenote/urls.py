from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import message
import stream
from user_account import urls as user_account_urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tubenote.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/account/', include(user_account_urls)),
    url(r'^api/message/', include(message.urls)),
    url(r'^api/stream/', include(stream.urls)),
)
