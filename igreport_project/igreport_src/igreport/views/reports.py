#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8

from django.http import HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required

from django.template import RequestContext
from igreport.models import IGReport, Category
from igreport.models import UserProfile

from rapidsms.contrib.locations.models import Location
from datetime import datetime

@require_GET
@login_required
def show_reports(request, **kwargs):
    report_filter = request.GET.get('filter', 'all')
    print report_filter
    reports = IGReport.objects.all()

    if not request.user.is_staff:
        try:
            reports = reports.filter(district=request.user.get_profile().district)
        except UserProfile.DoesNotExist:
            return HttpResponse('', status=404)

    if report_filter == 'incomplete':
        reports = reports.filter(completed=False)
    elif report_filter == 'completed':
        reports = reports.filter(completed=True, synced=False)
    elif report_filter == 'synced':
        reports = reports.filter(synced=True)


    reports = reports.order_by('synced', 'completed', '-datetime')

    return render_to_response("igreport/igreports.html", {\
        'reports':reports
    }, context_instance=RequestContext(request))


@require_POST
@login_required
def submit_report(request, report_id):
    try:
        valid_district = False
        report = get_object_or_404(IGReport, pk=long(report_id))
        if request.POST['category']:
            report.category = Category.objects.get(id=long(request.POST['category']))
        else:
            report.category = None

        if request.POST['district']:
            report.district = Location.objects.get(id=long(request.POST['district']))
        else:
            report.district = None

        valid_district = True
        if request.POST['subcounty']:
            report.subcounty = Location.objects.get(id=long(request.POST['subcounty']))
        else:
            report.subcounty = None

        report.subject = request.POST['subject'] or ''
        report.report = request.POST['report'] or ''
        if request.POST['whendatetime']:
            report.when_datetime = datetime.strptime(request.POST['whendatetime'], '%m/%d/%Y')
        else:
            report.when_datetime = None

        report.save()
    except ValueError:
        return HttpResponse('whendatetime', status=400)
    except Location.DoesNotExist:
        if valid_district:
            return HttpResponse('subcounty', status=400)
        else:
            return HttpResponse('district', status=400)
    except Category.DoesNotExist:
        return HttpResponse('category', status=400)

    return HttpResponse('OK',
            status=200)

