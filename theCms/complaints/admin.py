from django.contrib import admin

from complaints.models import *

admin.site.register(Complaint)
admin.site.register(Update)
admin.site.register(District)
admin.site.register(ComplaintSource)
admin.site.register(Entity)
admin.site.register(Offence)