from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site
from django.contrib.auth.models import User
from django.conf import settings

from script.models import Script, ScriptStep
from poll.models import Poll

class Command(BaseCommand):
    help = 'Create the basic script in the database prompting the user for basic information'

    def handle(self, *files, **options):
        print "updating name question to: %s" % settings.HOTLINE_NAME_QUESTION
        print "updating location question to: %s" % settings.HOTLINE_LOCATION_QUESTION
        print "updating confirmation message to: %s" % settings.HOTLINE_CONFIRMATION_MESSAGE

        script, _ = Script.objects.get_or_create(slug='hotline_script')
        script.name = 'IGReport Hotline Script'
        script.sites.clear()
        script.sites.add(Site.objects.get_current())
        script.enabled = True
        script.save()

        script.steps.all().delete()

        user = User.objects.all()[0]

        name_poll, _ = Poll.objects.get_or_create(name='hotline_name', defaults={'user':user})
        name_poll.question = settings.HOTLINE_NAME_QUESTION
        name_poll.type = Poll.TYPE_TEXT
        name_poll.default_response = ''
        name_poll.user = user
        name_poll.save()

        name_poll.sites.add(Site.objects.get_current())
        name_step, _ = ScriptStep.objects.get_or_create(script=script,order=1)
        name_step.message = ''
        name_step.poll = name_poll
        name_step.rule = ScriptStep.RESEND_MOVEON
        name_step.start_offset = 0
        name_step.retry_offset = 3600
        name_step.num_tries = 1
        script.steps.add(name_step)

        location_poll, _ = Poll.objects.get_or_create(name='hotline_location', defaults={'user':user})
        location_poll.question = settings.HOTLINE_LOCATION_QUESTION
        location_poll.type = Poll.TYPE_LOCATION
        location_poll.user = user
        location_poll.save()
        location_poll.sites.add(Site.objects.get_current())
        location_step, _ = ScriptStep.objects.get_or_create(script=script,order=2)                                                
        location_step.poll = location_poll
        location_step.message = ''
        location_step.rule = ScriptStep.RESEND_MOVEON
        location_step.start_offset = 0
        location_step.retry_offset = 3600
        location_step.num_tries = 1
        location_step.save()
        script.steps.add(location_step)

        confirm_step, _ = ScriptStep.objects.get_or_create(script=script, order=3)
        confirm_step.message = settings.HOTLINE_CONFIRMATION_MESSAGE
        confirm_step.rule = ScriptStep.WAIT_MOVEON
        confirm_step.start_offset = 0
        confirm_step.giveup_offset = 0
        confirm_step.save()
        script.steps.add(confirm_step)
