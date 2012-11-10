from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from rapidsms_httprouter.urls import urlpatterns as router_urls
from ureport.urls import urlpatterns as ureport_urls
from contact.urls import urlpatterns as contact_urls
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_change
from tracking.urls import urlpatterns as tracking_urls
from generic.urls import urlpatterns as generic_urls
from django.views.generic.simple import direct_to_template
from ussd.urls import urlpatterns as ussd_urls
from message_classifier.urls import urlpatterns as class_urls
#from script.urls import urlpatterns as script_urls
admin.autodiscover()

urlpatterns = patterns('',
    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^admin/', include(admin.site.urls)),
    (r'^polls/', include('poll.urls')),
) + router_urls


if settings.DEBUG:
    urlpatterns += patterns('',
        # helper URLs file that automatically serves the 'static' folder in
        # INSTALLED_APPS via the Django static media server (NOT for use in
        # production)
        (r'^', include('rapidsms.urls.static_media')),
    )

