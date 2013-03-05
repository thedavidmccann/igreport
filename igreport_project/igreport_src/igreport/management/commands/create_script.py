from django.conf import settings
from django.db import transaction
from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from igreport import questions
from script.models import Script, ScriptStep
from poll.models import Poll

class Command(BaseCommand):

    def handle(self, *files, **options):

        conf = questions.translations
        user = User.objects.all()[0]
        site = Site.objects.get_current()

        with transaction.commit_on_success():
            try:
                for language in conf.keys():

                    params = conf[language]

                    if not params.has_key('COMPLAINT_QUESTION') or \
                    not params.has_key('ACCUSED_QUESTION') or \
                    not params.has_key('AMOUNT_QUESTION') or \
                    not params.has_key('DISTRICT_QUESTION') or \
                    not params.has_key('NAME_QUESTION'):
                        raise Exception('Configuration for language "%s" is incomplete' % language)

                    print '************ [%s] Language configuration ************' % language
                    t = (params['COMPLAINT_QUESTION'], params['ACCUSED_QUESTION'], params['DISTRICT_QUESTION'], params['AMOUNT_QUESTION'], params['NAME_QUESTION'], params['CONFIRMATION_MESSAGE'])
                    print 'COMPLAINT_QUESTION: %s\nACCUSED_QUESTION: %s\nDISTRICT_QUESTION: %s\nAMOUNT_QUESTION: %s\nNAME_QUESTION: %s\nCONFIRMATION_MESSAGE: %s\n' % t

                    slug_name = 'hotline_script_%s' % language
                    description = 'IGReport Hotline Script (%s)' % language
                    script, created = Script.objects.get_or_create(slug=slug_name, defaults=dict(name=description, enabled=True))
                    if not created:
                        print 'Script for language "%s" appears to be existing.. Will skip it!\n' % language
                        continue
                    script.sites.add(site)

                    # What is your complaint?
                    complaint_poll = Poll.objects.create(name='hotline_complaint', user=user, question=params['COMPLAINT_QUESTION'], type=Poll.TYPE_TEXT, default_response='')
                    complaint_poll.sites.add(site)
                    complaint_step = ScriptStep.objects.create(script=script, order=0, message='', poll=complaint_poll, rule=ScriptStep.RESEND_MOVEON, \
                                    start_offset=0, retry_offset=3600, giveup_offset=3600, num_tries=1)
                    script.steps.add(complaint_step)

                    # Who are you reporting?
                    accused_poll = Poll.objects.create(name='hotline_accused', user=user, question=params['ACCUSED_QUESTION'], type=Poll.TYPE_TEXT, default_response='')
                    accused_poll.sites.add(Site.objects.get_current())
                    accused_step = ScriptStep.objects.create(script=script, order=1, message='', poll=accused_poll, rule=ScriptStep.RESEND_MOVEON, \
                                    start_offset=0, retry_offset=3600, giveup_offset=3600, num_tries=1)
                    script.steps.add(accused_step)

                    # District question
                    district_poll = Poll.objects.create(name='hotline_district', user=user, question=params['DISTRICT_QUESTION'], type=Poll.TYPE_LOCATION, default_response='')
                    district_poll.sites.add(Site.objects.get_current())
                    district_step = ScriptStep.objects.create(script=script, order=2, poll=district_poll, message='', rule=ScriptStep.STRICT_MOVEON, \
                                         start_offset=0, retry_offset=3600, num_tries=1, giveup_offset=3600)
                    script.steps.add(district_step)

                    # Amount involved
                    amount_poll = Poll.objects.create(name='hotline_amount', user=user, question=params['AMOUNT_QUESTION'], type=Poll.TYPE_TEXT, default_response='')
                    amount_poll.sites.add(Site.objects.get_current())
                    amount_step = ScriptStep.objects.create(script=script, order=3, poll=amount_poll, rule=ScriptStep.STRICT_MOVEON, \
                                        start_offset=0, retry_offset=3600, num_tries=1, giveup_offset=3600)
                    script.steps.add(amount_step)

                    # What is your name
                    name_poll = Poll.objects.create(name='hotline_name', user=user, question=params['NAME_QUESTION'], type=Poll.TYPE_TEXT)
                    name_poll.sites.add(Site.objects.get_current())
                    name_step = ScriptStep.objects.create(script=script, order=4, poll=name_poll, message='', rule=ScriptStep.RESEND_MOVEON, \
                                    start_offset=0, retry_offset=3600, num_tries=1, giveup_offset=3600)
                    script.steps.add(name_step)

            except Exception as err:
                transaction.rollback()
                print 'ERROR: %s\n****No changes made to database' % err.__str__()

