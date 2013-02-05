#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8

from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from igreport.models import IGReport
from django.utils import simplejson
from django.conf import settings


@require_POST
@login_required
def sync_report(request, report_id):
    report = get_object_or_404(IGReport, pk=long(report_id))
    # username
    # password

    # accused
    # accused_gender
    # district
    # report, offences
    # !complainant should not be anonymous
    # !dupes must be handled on cms
    # !report vs. offences?
    # !category? date? phone number? comments?
    # no security (and key errors for missing username/pass)

    # {"accused":"blah",
    #  "accused_gender":"M",
    #  "accused_ent_type":"P",
    #  "district":"kampala",
    #  "report":"test",
    #  "offences":"test",
    #  "username":"admin",
    #  "password":"admin"}
    if report.completed:
        report_data = {}


        report_data['accused'] = report.subject
        report_data['accused_gender'] = 'N'  # don't collect gender
        report_data['accused_ent_type'] = 'P'  # don't collect type
        report_data['district'] = report.district.name
        # CATEGORIES
        report_data['offences'] = ';'.join(report.comments.values_list('comment', flat=True))  # this is wrong
        report_data['username'] = settings.CMS_USER
        report_data['password'] = settings.CMS_PASSWORD
        report_data['complainant'] = report.connection.identity
        report_data['report'] = report.report

        # json doesn't know how to serialize datetimes, which means this sync code doesn't
#         report_data['complaint_date'] = report.when_datetime

        report_data = simplejson.dumps(report_data)

        cms_url = settings.CMS_URL
        # POST here

        report.synced = True
        report.save()
        return HttpResponse('OK',
            status=200)
    else:
        return HttpResponse('', status=400)
