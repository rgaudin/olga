from django.conf.urls.defaults import *

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^/?', include('scan.urls')),

    # django admin
    (r'^admin/', include(admin.site.urls)),
)
