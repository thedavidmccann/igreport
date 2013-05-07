from django.contrib import admin
from django.contrib.sites.models import Site
from eav.models import Attribute, Value, EnumValue, EnumGroup
from generic.models import Dashboard, Module, ModuleParams, StaticModuleContent
from script.models import ScriptProgress,ScriptStep,Script
from rapidsms.models import App, Backend, Connection, Contact
from poll.models import Poll, Response, Category as PollCategory, Rule, ResponseCategory,Translation
from rapidsms_httprouter.models import Message

# unregister some apps
# unregister apps that we don't manage from admin

def unregister_apps():
    # eav
    admin.site.unregister(Attribute)
    admin.site.unregister(Value)
    admin.site.unregister(EnumValue)
    admin.site.unregister(EnumGroup)
    
    # generic
    admin.site.unregister(Dashboard)
    admin.site.unregister(Module)
    admin.site.unregister(ModuleParams)
    admin.site.unregister(StaticModuleContent)
    
    # script
    admin.site.unregister(ScriptProgress)
    admin.site.unregister(Script)
    admin.site.unregister(ScriptStep)
    
    # rapidsms
    admin.site.unregister(App)
    admin.site.unregister(Backend)
    admin.site.unregister(Connection)
    admin.site.unregister(Contact)
    
    # poll
    admin.site.unregister(Poll)
    admin.site.unregister(Response)
    admin.site.unregister(PollCategory)
    admin.site.unregister(Rule)
    admin.site.unregister(ResponseCategory)
    admin.site.unregister(Translation)
    
    # rapidsms_httprouter
    admin.site.unregister(Message)
    
    # site
    admin.site.unregister(Site)