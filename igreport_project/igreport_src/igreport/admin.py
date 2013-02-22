from django.conf import settings
from django.contrib import admin
from django.forms import ModelForm, ModelChoiceField
from rapidsms.contrib.locations.models import Location
from igreport.models import IGReport, UserProfile, Category
from igreport import media
from igreport.html.admin import ListStyleAdmin

class IGReportAdmin(admin.ModelAdmin, ListStyleAdmin):

    list_display = ['message', 'accused', 'amount_formatted', 'sender', 'report_time', 'options']
    list_filter = ['datetime']
    #date_hierarchy = ['datetime']
    search_fields = ['reference_number', 'connection__identity']
    actions = None
    Media = media.JQueryUIMedia
    change_list_template = 'igreport/change_list.html'
    change_list_results_template = 'igreport/change_list_results.html'

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
        width = ''
        if len(text) > 50:
            width = '300px'
        else:
            html = text
        style = ''
        if width:
            style += 'width:%s;' % width
        if style:
            style = ' style="%s"' % style
        html = '<div id="rpt_%s"%s>%s</div>' % (obj.id, style, text)
        return html

    message.short_description = 'Report'
    message.allow_tags = True

    def sender(self, obj):
        msisdn = obj.connection.identity
        t = (obj.id, msisdn, msisdn, msisdn)
        html = '<a href="" onclick="smsp(%s,\'%s\');return false;" \
               style="font-weight:bold" title="Click to Send SMS to %s">%s</a>' % t
        return html
    
    sender.short_description = 'Sender'
    sender.admin_order_field = 'connection'
    sender.allow_tags = True

    def amount_formatted(self, obj):
        if obj.amount:
            return int(obj.amount)
        return 'NA'
    
    amount_formatted.short_description = 'Amount'
    amount_formatted.admin_order_field = 'amount'

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
    
    def get_row_css(self, obj, index):
        if obj.completed:
            return ' rpt-completed'
        if obj.synced:
            return ' rpt-synced'
        return ''

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
        context = {'title': title, 'include_file':'igreport/report.html', 'bottom_js':'rptsetc()', 'buttons': buttons}
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
