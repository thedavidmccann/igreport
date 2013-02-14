import re
import json
import traceback
from django.conf import settings
from django.db import transaction
from django.utils import simplejson
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST, require_GET
from rapidsms.contrib.locations.models import Location, LocationType
from igreport.models import IGReport, Category, Comment

def ajax_success(msg=None, js_=None):
	if msg is None:
		msg = 'OK'
	
	if js_ is None:
		js = '{error:false, msg:"%s"}' % msg
	else:
		js = '{error:false, msg:"%s", %s}' % (msg, js_)
	return HttpResponse(js, mimetype='text/plain')

def ajax_error(msg=None):
	if msg is None:
		msg = 'ERROR'
	
	js = '{error:true, msg:%s}' % json.dumps(msg)
	return HttpResponse(js, mimetype='text/plain')

@login_required
@require_GET
def get_report(request):

	if not request.GET.has_key('id'):
		return ajax_error('Bad Request')
	
	report_id = request.GET['id']
	if not re.search('^[0-9]+$', report_id):
		return ajax_error('Invalid report ID')
	
	try:
		r = IGReport.objects.get(pk=report_id)

		js = {
			'accused': r.subject if r.subject else '',
			'report': r.report if r.report else '',
			'amount_ff': r.amount_freeform if r.amount_freeform else '',
			'amount': str( int(r.amount) ) if r.amount else '',
			'sc_ff': r.subcounty_freeform if r.subcounty_freeform else '',
			'subcounty_id': r.subcounty_id if r.subcounty_id else '',
			'district_id': r.district_id if r.district_id else '',
			'when_ff': r.when_freeform if r.when_freeform else '',
			'when': r.when_datetime.strftime('%Y-%m-%d') if r.when_datetime else '',
			'date': r.datetime.strftime('%d/%m/%Y %H:%M'),
			'sender': r.connection.identity,
		}
		js_rpt = simplejson.dumps(js)
		
		''' get districts '''
		objs = Location.objects.filter(type='district').order_by('name')
		l = [ '{id:%s,name:%s}' % (d.id, json.dumps(d.name)) for d in objs ]
		js_districts = '[%s]' % ','.join(l)

		''' get sub-counties '''
		objs = Location.objects.filter(type='sub_county').order_by('name')
		l = [ '{id:%s,name:%s}' % (d.id, json.dumps(d.name)) for d in objs ]
		js_subcty = '[%s]' % ','.join(l)

		''' the selected categories '''
		curr_categories = [c.id for c in r.categories.all()]
		
		''' all categories '''
		objs = Category.objects.all()
		l=list()
		for c in objs:
			checked='false'
			if curr_categories.__contains__(c.id):
				checked = 'true'
			l.append( '{id:%s,name:%s,checked:%s}' % (c.id, json.dumps(c.name), checked) )
		
		js_cat = '[%s]' % ','.join(l)
		
		''' comments '''
		objs = Comment.objects.filter(report=r)
		l = [ '{user:%s,date:%s,comment:%s}' %
		     (json.dumps(c.user.username),
		      json.dumps(c.datetime.strftime('%d/%m/%Y')),
		      json.dumps(c.comment)) for c in objs ]
		js_comments = '[%s]' % ','.join(l)
		
		js_text = 'res:{ rpt:%s,dist:%s,scty:%s,cat:%s,comm:%s }' % (
			js_rpt, js_districts, js_subcty, js_cat, js_comments
		)
		return ajax_success('OK', js_text)
	except IGReport.DoesNotExist:
		return ajax_error('The requested report was not found')
	except Exception as err:
		return ajax_error(err.__str__())
	
	return ajax_error('Not done')

@login_required
@require_POST
@csrf_exempt
def update_report(request):
	
	try:
		f = request.POST
		if 	not f.has_key('id') or \
			not f.has_key('report') or \
			not f.has_key('accused') or \
			not f.has_key('amount') or \
			not f.has_key('date') or \
			not f.has_key('dist') or \
			not f.has_key('sc'):
				return ajax_error('Incomplete form submission')
		
		''' validate all fields '''
		if not re.search('^[0-9]+$', f['id']):
			ajax_error('Report ID not valid')
		
		try:
			report = IGReport.objects.get(id=f['id'])
			if report.synced:
				return ajax_error('Modifications to this report are not allowed!')
		except IGReport.DoesNotExist:
			return ajax_error('The requested report does not exist')
			
		if len(f['report']) < 1:
			ajax_error('Report not valid')
		
		if len(f['accused']) < 1:
			ajax_error('Accused not valid')
		
		if not re.search('^[0-9]+$', f['amount']):
			ajax_error('Amount not valid')

		if not re.search('^\d{4}-\d{2}-\d{2}$', f['date']):
			ajax_error('Date of incident not valid')

		if not re.search('^[0-9]+$', f['dist']):
			ajax_error('District not valid')

		if not re.search('^[0-9]+$', f['sc']):
			ajax_error('Subcounty not valid')
		
		categories = list()
		if f.has_key('catl'):
			l = re.compile(',').split(f['catl'])
			for i in l:
				if not re.search('^[0-9]+$', i):
					return ajax_error('Invalid category ID "%s"' % i)
				categories.append(i)
		
		report.report = f['report']
		report.subject = f['accused']
		report.amount = f['amount']
		report.when_datetime = f['date']
		report.district_id = f['dist']
		report.subcounty_id = f['sc']
		report.completed = True
		
		''' save it '''
		try:
			with transaction.commit_on_success():
				report.save()
				report.categories.clear()
				if categories:
					for c in categories:
						report.categories.add( Category.objects.get(id=c) )
				# the comment
				
				if len(f['comments']):
					comment = Comment(
						user = request.user,
						report = report,
						comment = f['comments']
					)
					comment.save()
			
		except Exception as err:
			transaction.rollback()
			#error = traceback.format_exc()
			return ajax_error('#1:%s' % err.__str())
		
		return ajax_success('it worked!')
		
	except Exception as err:
		return ajax_error('#2:%s' % err.__str__())
	
	return ajax_error('Not done')

@login_required
@require_GET
def sync_report(request):
	
	try:
		if not request.GET.has_key('id'):
			return ajax_error('Bad request')
		
		report_id = request.GET['id']

		report = IGReport.objects.get(pk=report_id)
		if report.synced:
			return ajax_error('This report is already synced')
		
		if not report.completed:
			return ajax_error('This report can not be synced because it is incomplete')
			
		data = dict()
		data['report'] = report.report
		data['accused'] = report.subject
		data['accused_gender'] = 'N'  # don't collect gender
		data['accused_ent_type'] = 'P'  # don't collect type
		data['district'] = report.district.name
		data['offences'] = ','.join(report.categories.values_list('name', flat=True))
		data['username'] = settings.CMS_USER
		data['password'] = settings.CMS_PASSWORD
		data['complainant'] = report.connection.identity
		data['complaint_date'] = report.when_datetime.strftime('%Y-%m-%d %H:%M:%S')
		
		text = simplejson.dumps(data)
		# POST by HTTP
		# David and Noel have not yet agreed on how to handle syncing
		return ajax_success('Syncing not yet implemented')
	
	except IGReport.DoesNotExist:
		return ajax_error('Invalid report ID')
		
	except Exception as err:
		return ajax_error(err.__str__())
	
	return ajax_error('Not done')		