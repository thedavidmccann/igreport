#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8

from rapidsms.apps.base import AppBase
from script.models import ScriptProgress, Script
from .models import IGReport

class App(AppBase):
    def handle (self, message):
        # dump new connections in report collector
        if (not ScriptProgress.objects.filter(script__slug='hotline_script', connection=message.connection).exists()):
            ScriptProgress.objects.create(script=Script.objects.get(slug='hotline_script'), connection=message.connection)
            IGReport.objects.create(connection=message.connection, report=message.text)
            return True

        return False
