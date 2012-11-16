from rapidsms.apps.base import AppBase

from script.models import ScriptProgress

class App(AppBase):
    def handle (self, message):

        #dump new connections in report collector
        if not ScriptProgress.objects.filter(script__slug='hotline_script', connection=message.connection).exists():
            ScriptProgress.objects.create(script=Script.objects.get(slug='hotline_script'), connection=message.connection)
            return True

        return False
            