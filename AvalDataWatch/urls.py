from django.conf.urls import patterns, include, url
from AvalDataWatch.views import pgtitle, precip, mscharts, region
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^start/$', pgtitle),
                       url(r'^precip/$', precip),
                       url(r'^mscharts/$', mscharts),
                       url(r'^region/$', region),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    # Examples:
    # url(r'^$', 'AvalDataWatch.views.home', name='home'),
    # url(r'^AvalDataWatch/', include('AvalDataWatch.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
