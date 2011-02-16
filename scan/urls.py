
from django.conf.urls.defaults import *
from django.conf import settings

import views

urlpatterns = patterns('',
    url(r'^/?$', views.scan, name='scan_scan'),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^scans/(?P<path>.*)$', 'django.views.static.serve', \
        {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )

