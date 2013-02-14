from django.conf import settings
from django.contrib import admin
from django.forms import ModelForm, ModelChoiceField
from rapidsms.contrib.locations.models import Location
from igreport.models import IGReport, UserProfile, Category
from igreport import media

class IGReportAdmin(admin.ModelAdmin):
	
	list_display = ['message', 'accused', 'amount', 'sender', 'report_time', 'options']
	list_filter = ['datetime']
	#date_hierarchy = ['datetime']
	search_fields = ['connection__identity']
	actions = None
	Media = media.JQueryUIMedia
	change_list_template = 'igreport/change_list.html'
	
	def __init__(self, *args, **kwargs):
		super(IGReportAdmin, self).__init__(*args, **kwargs)
		self.list_display_links = (None,)
		
	def accused(self, obj):
		return obj.subject
	
	accused.short_description = 'Accused'
	
	def report_time(self, obj):
		return obj.datetime.strftime('%d/%m/%Y %H:%M')
	
	report_time.short_description = 'Report Date'
	report_time.admin_order_field = 'datetime'
	
	def message(self, obj):
		text = obj.report
		if len(text) > 50:
			html = '<div style="width:300px">%s</div>' % text
		else:
			html=text
		return html
	
	message.short_description = 'Report'
	message.allow_tags = True

	def sender(self, obj):
		msisdn = obj.connection.identity	
		return msisdn
	
	sender.short_description = 'Sender'
	sender.admin_order_field = 'connection'

	def options(self, obj):
		html = ''
		if not obj.synced:
			link = '<a href="" onclick="editrpt(%s);return false;" title="Edit Report"><img src="%s/igreport/img/edit.png"></a>&nbsp;&nbsp;&nbsp;' % (obj.id, settings.STATIC_URL)
			html += link
		
		if obj.completed and not obj.synced:
			link = '<a href="" onclick="syncit(%s);return false;" title="Sync Report"><img src="%s/igreport/img/sync.png"></a>' % (obj.id, settings.STATIC_URL)
			html += link
		
		return html
	
	options.short_description = 'Options'
	options.allow_tags = True

	def has_add_permission(self, request):
		return False
	
	def has_delete_permission(self, request, obj=None):
		return False
	
	def changelist_view(self, request, extra_context=None):
		title = 'Reports'
		
		buttons = [ {'label': 'All Reports', 'link': '?'},
			{'label': 'Completed', 'link': '?completed=1'},
			{'label': 'Synced', 'link': '?synced=1'},
			{'label': 'Refresh', 'link': '?'} ]
		context = {'title': title, 'include_file':'igreport/report.html', 'buttons': buttons}
		return super(IGReportAdmin, self).changelist_view(request, extra_context=context)

class UserProfileForm(ModelForm):
    district = ModelChoiceField(Location.objects.filter(type__name='district').order_by('name'))
    class Meta:
        model = UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    form = UserProfileForm

admin.site.register(IGReport, IGReportAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(Category)
