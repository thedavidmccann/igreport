#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8

import difflib
from rapidsms.apps.base import AppBase
from script.models import ScriptProgress, Script
from rapidsms.models import Contact
from django.conf import settings
from .models import IGReport

class App(AppBase):
    
    def handle (self, message):
        entry = ScriptProgress.objects.filter(script__slug__startswith='hotline_script', connection=message.connection)
        text = (message.text).lower()
        
        if (not entry.exists()):
            matches = difflib.get_close_matches(text, settings.REPORT_KEYWORDS.keys(), 1)

            if not matches:
                return False
            
            keyword = matches[0]
            language = settings.REPORT_KEYWORDS[keyword]
            slug_name = 'hotline_script_%s' % language
            
            ScriptProgress.objects.create(script=Script.objects.get(slug=slug_name), connection=message.connection)
            report = IGReport.objects.create(connection=message.connection, keyword=message.text)
            contact = Contact(name=message.connection.identity, language=language)
            contact.save()
            report.connection.contact = contact
            report.connection.save()
            
            return True

        return False
