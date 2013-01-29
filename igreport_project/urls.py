#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8

from django.views.generic.simple import direct_to_template
from django.conf.urls.defaults import *
from django.conf import settings
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import password_change
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic.simple import direct_to_template
from django.contrib.auth.decorators import login_required
from rapidsms_httprouter.views import receive
from django.views.decorators.http import require_POST

admin.autodiscover()

from igreport.views.test import check_progress
from igreport.views.messages import show_messages
from igreport.views.reports import show_reports, submit_report
from igreport.views.sync import sync_report
from igreport.views.utils import show_categories, show_districts, show_subcounties
from django.contrib.auth.views import login, logout

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),

    url('^$', direct_to_template, {'template':'igreport/index.html'}),
    url('^login$', require_POST(login)),
    url('^logout$', require_POST(logout)),

    (r'^test/$', login_required(direct_to_template), {'template':'igreport/tester.html'}),
    url('^test/progress/\d*/$', check_progress),
    url('^messages/(?P<identity>\d{7,20})/$', show_messages),
    url('^messages/(?P<identity>\d{7,20})/(?P<start_year>\d{4})/(?P<start_month>\d{2})/(?P<start_day>\d{2})/(?P<start_hour>\d{2})/(?P<start_minute>\d{2})/(?P<start_second>\d{2})/\d*/$', show_messages),
    url('^messages/(?P<identity>\d{7,20})/(?P<start_year>\d{4})/(?P<start_month>\d{2})/(?P<start_day>\d{2})/(?P<start_hour>\d{2})/(?P<start_minute>\d{2})/(?P<start_second>\d{2})/(?P<end_year>\d{4})/(?P<end_month>\d{2})/(?P<end_day>\d{2})/(?P<end_hour>\d{2})/(?P<end_minute>\d{2})/(?P<end_second>\d{2})/$', show_messages),

    (r'^reports/$', login_required(direct_to_template), {'template':'igreport/reports.html'}),
    url('^categories/$', show_categories),
    url('^districts/$', show_districts),
    url('^subcounties/$', show_subcounties),
    url('^igreports/$', show_reports),
    url('^igreports/(?P<report_id>\d*)/$', submit_report),
    url('^igreports/(?P<report_id>\d*)/sync/$', sync_report),

    url("^router/receive", receive),
)


if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()


