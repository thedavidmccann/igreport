#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8

from script.utils.handling import find_closest_match, find_best_response
from script.models import ScriptSession
from rapidsms.contrib.locations.models import Location
from poll.models import Poll

def handle_report(**kwargs):
    from .models import IGReport
    subject_poll = Poll.objects.get(scriptstep__script__slug='hotline_script', name='hotline_subject')
    amount_poll = Poll.objects.get(scriptstep__script__slug='hotline_script', name='hotline_amount')
    district_poll = Poll.objects.get(scriptstep__script__slug='hotline_script', name='hotline_district')
    subcounty_poll = Poll.objects.get(scriptstep__script__slug='hotline_script', name='hotline_subcounty')
    when_poll = Poll.objects.get(scriptstep__script__slug='hotline_script', name='hotline_when')

    connection = kwargs['connection']
    progress = kwargs['sender']
    session = ScriptSession.objects.filter(script=progress.script, connection=connection).latest('end_time')

    report = IGReport.objects.filter(connection=connection).latest('datetime')
    report.subject = find_best_response(session, subject_poll)
    report.when_freeform = find_best_response(session, when_poll)
    report.district = find_best_response(session, district_poll)
    report.amount_freeform = find_best_response(session, amount_poll)

    report.subcounty_freeform = find_best_response(session, subcounty_poll)
    if report.subcounty_freeform:
        report.subcounty = find_closest_match(report.subcounty_freeform, Location.objects.filter(type__name='sub_county'))

    report.save()

def igreport_pre_save(sender, **kwargs):
    instance = kwargs['instance']
    if instance.category and instance.district and instance.subcounty and instance.when_datetime and instance.amount:
        instance.completed = True
    else:
        instance.completed = False



