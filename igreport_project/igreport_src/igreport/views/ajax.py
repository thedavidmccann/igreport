import re
import json
from django.utils import simplejson
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.cache import never_cache
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from rapidsms.contrib.locations.models import Location, LocationType
from rapidsms_httprouter.models import Message
from django.conf import settings
from igreport.models import IGReport, Currency, Category, Comment

def ajax_success(msg=None, js_=None):
    if msg is None:
        msg = 'OK'

    if js_ is None:
        js = '{error:false, msg:"%s"}' % msg
    else:
        js = '{error:false, msg:"%s", %s}' % (msg, js_)
    return HttpResponse(js, mimetype='text/plain', status=200)

@login_required
@require_GET
@never_cache
def get_report(request, report_id):

    try:
        r = get_object_or_404(IGReport, pk=report_id)
	default_currency = get_object_or_404(Currency, code=settings.DEFAULT_CURRENCY)

        js = dict(accused = r.subject or '', report = r.report or '', amount_ff = r.amount_freeform or '', amount = str(int(r.amount)) if r.amount>=0 else '', district_ff=r.district_freeform or '', district_id = r.district_id or  '', date = r.datetime.strftime('%d/%m/%Y %H:%M'), sender= r.connection.identity, names = r.names or '', currency_id=r.currency.id if r.currency else default_currency.id)
        js_rpt = simplejson.dumps(js)

        ''' get districts '''
        objs = Location.objects.filter(type='district').order_by('name')
        l = [ '{id:%s,name:%s}' % (d.id, json.dumps(d.name)) for d in objs ]
        l.insert(0, '{id:"",name:""}')
        js_districts = '[%s]' % ','.join(l)

        ''' get currencies '''
        objs = Currency.objects.all().order_by('name')
        l = [ '{id:%s,code:%s,name:%s}' % (d.id, json.dumps(d.code), json.dumps(d.name)) for d in objs ]
        l.insert(0, '{id:"",code:"",name:""}')
        js_currencies = '[%s]' % ','.join(l)

        ''' the selected categories '''
        curr_categories = [c.id for c in r.categories.all()]

        ''' all categories '''
        objs = Category.objects.all()
        l = list()

        for c in objs:
            checked='false'
            if curr_categories.__contains__(c.id):
                checked = 'true'
            l.append( '{id:%s,name:%s,checked:%s}' % (c.id, json.dumps(c.name), checked) )

        js_cat = '[%s]' % ','.join(l)

        ''' comments '''
        objs = Comment.objects.filter(report=r)
        l = [ '{user:%s,date:%s,comment:%s}' % (json.dumps(c.user.username), json.dumps(c.datetime.strftime('%d/%m/%Y')), json.dumps(c.comment)) for c in objs ]
        js_comments = '[%s]' % ','.join(l)

        js_text = 'res:{ rpt:%s,dist:%s,cat:%s,comm:%s,curr:%s }' % ( js_rpt, js_districts, js_cat, js_comments, js_currencies )

        return ajax_success('OK', js_text)
    except Exception as err:
        return HttpResponse(err.__str__(), status=500)

@login_required
@require_POST
@never_cache
def send_sms(request, report_id):

    report = get_object_or_404(IGReport, pk=report_id)

    if not request.POST.has_key('text'):
        return HttpResponse('Message not specified', status=400)

    text = request.POST['text'].strip()
    if not text or len(text) < 2:
        return HttpResponse('Message too short/not valid', status=400)

    try:
        Message.objects.create(direction='O', status='Q', connection=report.connection, text=text)
    except Exception as err:
        return HttpResponse(err.__str__(), status=500)

    return ajax_success()
