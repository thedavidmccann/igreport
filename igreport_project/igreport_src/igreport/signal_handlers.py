#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8

from script.utils.handling import find_closest_match, find_best_response
from script.models import ScriptSession
from rapidsms.contrib.locations.models import Location
from rapidsms_httprouter.models import Message
from igreport.questions import translations
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

    report.report = find_best_response(session, report_poll)
    report.subject = find_best_response(session, accused_poll)
    report.district = find_best_response(session, district_poll)
    report.amount_freeform = find_best_response(session, amount_poll)
    report.names = find_best_response(session, names_poll)
    connection.contact.name = report.names if report.names else connection.identity
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
    if instance.pk and len(instance.categories.all()) and instance.subject and instance.report and instance.district and instance.names and (instance.amount >= 0):
        instance.completed = True
    else:
        instance.completed = False



