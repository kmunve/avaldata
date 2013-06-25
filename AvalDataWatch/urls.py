from django.conf.urls import patterns, include, url
from AvalWeatherWatch.views import pgtitle, precip, mscharts
import settings
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^start/$', pgtitle),
                       url(r'^precip/$', precip),
                       url(r'^mscharts/$', mscharts),
                       url(r'^media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': settings.MEDIA_ROOT}),
    # Examples:
    # url(r'^$', 'AvalWeatherWatch.views.home', name='home'),
    # url(r'^AvalWeatherWatch/', include('AvalWeatherWatch.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
