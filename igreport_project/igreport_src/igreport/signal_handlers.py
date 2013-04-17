#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8

import re
import difflib
from script.utils.handling import find_closest_match, find_best_response
from script.models import ScriptSession
from rapidsms.contrib.locations.models import Location
from rapidsms_httprouter.models import Message
from igreport.questions import translations
from igreport import util
from poll.models import Poll

def handle_report(**kwargs):
    from .models import IGReport

    connection = kwargs['connection']
    report = IGReport.objects.filter(connection=connection).latest('datetime')
    language = report.connection.contact.language
    slug = 'hotline_script_%s' % language

    report_poll = Poll.objects.get(scriptstep__script__slug=slug, name='hotline_complaint')
    accused_poll = Poll.objects.get(scriptstep__script__slug=slug, name='hotline_accused')
    amount_poll = Poll.objects.get(scriptstep__script__slug=slug, name='hotline_amount')
    district_poll = Poll.objects.get(scriptstep__script__slug=slug, name='hotline_district')
    names_poll = Poll.objects.get(scriptstep__script__slug=slug, name='hotline_name')

    progress = kwargs['sender']
    session = ScriptSession.objects.filter(script=progress.script, connection=connection, end_time__isnull=False).latest('end_time')
    
    report.reference_number = util.get_reference_number(report.id)
    response = find_best_response(session, report_poll)
    report.report = response if response else ''
    report.subject = find_best_response(session, accused_poll)
    report.amount_freeform = find_best_response(session, amount_poll)
    report.names = find_best_response(session, names_poll)
    connection.contact.name = report.names if (report.names and len(report.names)<=100) else connection.identity
    
    district = find_best_response(session, district_poll)
    
    if district:
        if district_poll.type == Poll.TYPE_LOCATION:
            report.district = district
        else:
            report.district_freeform = district
            locations = Location.objects.filter(type='district')
            district_names = locations.values_list('name', flat=True)
            district_names_lower = [d.lower() for d in district_names]
            
            matches = difflib.get_close_matches(district.lower(), district_names_lower)
            if matches:
                district_obj = Location.objects.get(type__slug='district', name__iexact=matches[0].lower())
                report.district = district_obj
    
    connection.contact.save()
    report.save()
    Message.objects.create(\
        direction='O', \
        status='Q', \
        connection=connection, \
        application='script', \
        text=(translations[connection.contact.language]['CONFIRMATION_MESSAGE'] % {'reference_number':report.reference_number}))

def igreport_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    if instance.pk and len(instance.categories.all()) and instance.subject and instance.report and instance.district and instance.names:
        instance.completed = True
    else:
        instance.completed = False

