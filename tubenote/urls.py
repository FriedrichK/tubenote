from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

import message

import user_account

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'tubenote.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/account/', include(user_account.urls)),
)
