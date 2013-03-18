#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8

import urllib2
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from igreport.models import IGReport
from django.utils import simplejson
from django.conf import settings
from datetime import date, datetime


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
    if not report.completed:
        return HttpResponse('Report incomplete', status=400)
    
    try:
        report_data = { \
            'accused': report.subject,
            'accused_gender': 'N',  # don't collect gender
            'accused_ent_type': 'P',  # don't collect type
            'district': report.district.name,
            'offences': ','.join(report.categories.values_list('name', flat=True)),
            'username': settings.CMS_USER,
            'password': settings.CMS_PASSWORD,
            'complainant': report.connection.identity,
            'report': report.report,
            'reference_number': report.reference_number,
            'complaint_date': datetime.strftime(report.datetime, '%Y/%m/%d'),
        }
        if report.amount > 0:
            report_data['amount'] = report.amount

        report_data = simplejson.dumps(report_data)

        cms_url = settings.CMS_URL
        req = urllib2.Request(cms_url, report_data)
        response = urllib2.urlopen(req)
        json_response = response.read()
        json_object = simplejson.loads(json_response)

        print "WOOHOO %s" % json_response

        if (json_object['result'] != 'OK'):
            return HttpResponse('', status={'PD':403, 'RC':404, 'IE':500}[json_object['result']])

        report.synced = True
        report.save()
        return HttpResponse('OK', status=200)
    except Exception as err:
        return HttpResponse(err.__str__(), status=500)
