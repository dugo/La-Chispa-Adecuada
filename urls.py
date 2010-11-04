# coding=utf-8

from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

from settings import *

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),

    # """ Autentificacion """
    (r'^accounts/login/$','django.contrib.auth.views.login'),
    url(r'^accounts/logout/$','django.contrib.auth.views.logout',kwargs=dict(next_page=ROOT_URL) ),
    url(r'^accounts/profile/$','django.views.generic.simple.redirect_to',kwargs=dict(url=ROOT_URL) ),
    (r'^accounts/login/ajax/$',  'blog.views.loginajax'),
    
    # Media
    (r'^%s/(?P<path>.*)$' % settings.MEDIA_URL[1:-1], 'django.views.static.serve', {'document_root' : settings.MEDIA_ROOT}),
    
    (r'^', include('lachispaadecuada.blog.urls')),
)
