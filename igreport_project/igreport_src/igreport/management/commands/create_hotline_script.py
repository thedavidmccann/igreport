#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8

from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.conf import settings

from script.models import Script, ScriptStep
from poll.models import Poll

class Command(BaseCommand):
    help = 'Create the basic script in the database prompting the user for basic information'

    def handle(self, *files, **options):
        HOTLINE_NAME_QUESTION = settings.HOTLINE_NAME_QUESTION
        HOTLINE_DISTRICT_QUESTION = settings.HOTLINE_DISTRICT_QUESTION
        HOTLINE_SUBCOUNTY_QUESTION = settings.HOTLINE_SUBCOUNTY_QUESTION
        HOTLINE_WHEN_QUESTION = settings.HOTLINE_WHEN_QUESTION
        HOTLINE_CONFIRMATION_MESSAGE = settings.HOTLINE_CONFIRMATION_MESSAGE

        print "name question is: %s" % HOTLINE_NAME_QUESTION
        print "district question is: %s" % HOTLINE_DISTRICT_QUESTION
        print "subcounty question is: %s" % HOTLINE_SUBCOUNTY_QUESTION
        print "when question is: %s" % HOTLINE_WHEN_QUESTION
        print "confirmation message is: %s" % HOTLINE_CONFIRMATION_MESSAGE

        script = Script.objects.create(slug='hotline_script', name='IGReport Hotline Script', enabled=True)
        script.sites.add(Site.objects.get_current())

        user = User.objects.all()[0]

        # Welcome Message, asks for subect of report's name or organization
        subject_poll = Poll.objects.create(name='hotline_subject', user=user, question=HOTLINE_NAME_QUESTION, type=Poll.TYPE_TEXT, default_response='')
        subject_poll.sites.add(Site.objects.get_current())
        subject_step = ScriptStep.objects.create(script=script, order=0, message='', poll=subject_poll, rule=ScriptStep.RESEND_MOVEON, \
                        start_offset=0, retry_offset=3600, giveup_offset=3600, num_tries=1)
        script.steps.add(subject_step)

        # District question
        district_poll = Poll.objects.create(name='hotline_district', user=user, question=HOTLINE_DISTRICT_QUESTION, type=Poll.TYPE_LOCATION, default_response='')
        district_poll.sites.add(Site.objects.get_current())
        district_step = ScriptStep.objects.create(script=script, order=1, poll=district_poll, rule=ScriptStep.STRICT_MOVEON, \
                            start_offset=0, retry_offset=3600, num_tries=1, giveup_offset=3600)
        script.steps.add(district_step)

        # Subcounty question
        subcounty_poll = Poll.objects.create(name='hotline_subcounty', user=user, question=HOTLINE_SUBCOUNTY_QUESTION, type=Poll.TYPE_TEXT, default_response='')
        subcounty_poll.sites.add(Site.objects.get_current())
        subcounty_step = ScriptStep.objects.create(script=script, order=2, poll=subcounty_poll, message='', rule=ScriptStep.RESEND_MOVEON, \
                             start_offset=0, retry_offset=3600, num_tries=1, giveup_offset=3600)
        script.steps.add(subcounty_step)

        # When did the event reported on occur?
        when_poll = Poll.objects.create(name='hotline_when', user=user, question=HOTLINE_WHEN_QUESTION, type=Poll.TYPE_TEXT)
        when_poll.sites.add(Site.objects.get_current())
        when_step = ScriptStep.objects.create(script=script, order=3, poll=when_poll, message='', rule=ScriptStep.RESEND_MOVEON, \
                        start_offset=0, retry_offset=3600, num_tries=1, giveup_offset=3600)
        script.steps.add(when_step)

        # Thank the reporter, confirm receipt
        confirm_step = ScriptStep.objects.create(script=script, order=4, message=HOTLINE_CONFIRMATION_MESSAGE, rule=ScriptStep.WAIT_MOVEON, \
                           start_offset=0, giveup_offset=0)
        script.steps.add(confirm_step)
