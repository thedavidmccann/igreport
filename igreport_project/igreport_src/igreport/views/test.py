#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8

from django.http import HttpResponse
from django.core.management import call_command
from django.contrib.auth.decorators import login_required

@login_required
def check_progress(request):
    call_command('check_script_progress')
    return HttpResponse('OK',
        status=200)



