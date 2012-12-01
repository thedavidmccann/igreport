from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from rapidsms_httprouter.urls import urlpatterns as router_urls
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_change
from django.views.generic.simple import direct_to_template
from rapidsms_httprouter.views import console
#from script.urls import urlpatterns as script_urls
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^polls/', include('poll.urls')),
    url('^/$', console, name="rapidsms-dashboard"),
    url('^/$', console, name="rapidsms-logout"),
    url('^/$', console, name="rapidsms-login")
) + router_urls

#
#if settings.DEBUG:
#    urlpatterns += patterns('',
#        # helper URLs file that automatically serves the 'static' folder in
#        # INSTALLED_APPS via the Django static media server (NOT for use in
#        # production)
#        (r'^', include('rapidsms.urls.static_media')),
#    )

