from django.conf.urls.defaults import patterns, include, url
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from arts import urls as arts_urls

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'djangotests.views.home', name='home'),
    # url(r'^djangotests/', include('djangotests.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^arts/', include(arts_urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'^site_media/media/(?P<path>.*)$', 'serve', {'document_root': settings.MEDIA_ROOT})
    )
