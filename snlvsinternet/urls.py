from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',

    url(r'^snl/(?P<snl_key>\w+)$', 'snl.views.show', name='show_article'),
    url(r'^vs/(?P<snl_key>.+)$', 'snl.views.vs'),

    url(r'^$', 'snl.views.home', name='home'),
    url(r'^(?P<snl_key>.+)$', 'snl.views.vs', name='vs'),

    url(r'^admin/', include(admin.site.urls)),
)
