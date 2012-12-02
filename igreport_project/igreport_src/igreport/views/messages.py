#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8

from django.shortcuts import render_to_response
from django.template import RequestContext
from rapidsms_httprouter.models import Message
from datetime import datetime
from django.contrib.auth.decorators import login_required

@login_required
def show_messages(request, **kwargs):
    messages = Message.objects.filter(connection__identity=kwargs['identity'])
    if 'start_year' in kwargs:
        start_year = int(kwargs['start_year'])
        start_month = int(kwargs['start_month'])
        start_day = int(kwargs['start_day'])
        start_hour = int(kwargs['start_hour'])
        start_minute = int(kwargs['start_minute'])
        start_second = int(kwargs['start_second'])
        start_date = datetime(start_year, start_month + 1, start_day, start_hour, start_minute, start_second)

        if 'end_year' not in kwargs:
            messages = messages.filter(date__gte=start_date)
        else:
            end_year = int(kwargs['end_year'])
            end_month = int(kwargs['end_month'])
            end_day = int(kwargs['end_day'])
            end_hour = int(kwargs['end_hour'])
            end_minute = int(kwargs['end_minute'])
            end_second = int(kwargs['end_second'])
            end_date = datetime(end_year, end_month + 1, end_day, end_hour, end_minute, end_second)
            messages = messages.filter(date__range=(start_date, end_date))

    return render_to_response("igreport/messages.html", {\
        'messages':messages
    }, context_instance=RequestContext(request))
