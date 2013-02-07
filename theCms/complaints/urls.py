from django.conf.urls.defaults import *

urlpatterns = patterns('complaints.views',
    # Example:
    (r'^$', 'index',{'template_name':'index.html'} ),
	(r'^sync/$','sync_report'),
)