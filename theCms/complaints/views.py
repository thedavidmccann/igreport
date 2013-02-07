from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render_to_response, get_object_or_404
from django.views.decorators.http import require_POST, require_GET
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.template import RequestContext

from complaints.models import *
import itertools
try: from django.utils import simplejson as json
except ImportError: import json

def index(request, template_name):
	complaints = Complaint.objects.all()
	return render_to_response(template_name, locals(), context_instance=RequestContext(request))

@csrf_exempt
def sync_report(request):
	if request.method == 'POST':
		print request.raw_post_data
		resp = {'result':'', 'message':''}
		# Handle data
		data = json.loads(request.raw_post_data)
		data['accused'] = data['accused'].title()

		# Get user and basic auth
		user = authenticate(username=data['username'], password=data['password'])
		if user is not None:
			if user.is_active:pass
			else:
				resp['result'], resp['message'] = 'PD', 'Permission Denied'
				return HttpResponse(json.dumps(resp), mimetype='application/json')
		else:
			resp['result'], resp['message'] = 'PD', 'Permission Denied'
			return HttpResponse(json.dumps(resp), mimetype='application/json')

		# Check for related complaints and return data about those complaints
		try:
			accused_perms = [ ' '.join(p) for p in list(itertools.permutations(data['accused'].replace('  ', '').split(' '))) if len(p) > 1]
		except:
			accused_perms = [data['accused']]

		# get related complaints
		rcs = Complaint.objects.filter(complaint_reference__icontains='SMS', accused__name__in=accused_perms)
		if len(rcs):
			# Would probably return data from related complaints. A lot of data may have to be transfered here.
			# RECOMMENDATION: This must be done in Hotline before syncing. Complaints must be checked against other complaints that seem
			# to have duplicates in the sms hotline so that this is not done here.
			resp['result'], resp['message'] = 'RC', 'Related complaints exist'
			return HttpResponse(json.dumps(resp), mimetype='application/json')

		# Register complaint
		try:
			c = Complaint(
			registered_by=user,
			source_of_complaint=ComplaintSource.objects.get_or_create(name='SMS hotline')[0],
			complainant=Entity.objects.get_or_create(name='Anonymous')[0],
			accused=Entity.objects.get_or_create(name=data['accused'].title(), gender=data['accused_gender'],
			ent_type=data['accused_ent_type'])[0],
			# offences = , MAY HAVE TO DETERMINE WHO SHOULD REALLY CLASSIFY COMPLAINTS
			district=District.objects.get(name__icontains=data['district']),
			status='OG',
			report=(data['report'] + ' :(%s)' % data['offences']),
			)
			c.save()
			resp['result'], resp['message'] = 'OK', 'Success'

			# TO DO: Handle other requirements for the CMS
			# Submit complaint
			# Need to determine case officer to submit to ...
			# Create update object as should be
			# Submit complaint. To be done later ...

			return HttpResponse(json.dumps(resp), mimetype='application/json')
		except Exception, e:
			resp['result'], resp['message'] = 'IE', 'Internal Error: %s' % e
			return HttpResponse(json.dumps(resp), mimetype='application/json')


	return HttpResponseRedirect('/')
