from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_GET
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.decorators.cache import never_cache
from rapidsms.contrib.locations.models import Location
from igreport.models import IGReport, Currency

@login_required
@require_GET
@never_cache
def print_preview(request, report_id):

    try:
        r = get_object_or_404(IGReport, pk=report_id)
        
        default_currency, created = Currency.objects.get_or_create(code=settings.DEFAULT_CURRENCY['code'], defaults=dict(name=settings.DEFAULT_CURRENCY['name']))
        
        if r.currency:
            currency = r.currency.code
        else:
            currency = default_currency.code
        
        if r.amount:
            amount = str( int(r.amount) )
            
            if currency:
                amount = currency + amount
        else:
            amount = '__'
            
        if r.district_id:
            obj = get_object_or_404(Location, pk=r.district_id)
            district = obj.name
        else:
            district = ''

        report = dict(accused = r.subject or '(empty)', report = r.report or '(empty)', amount_ff = r.amount_freeform or '(empty)', amount=amount, district_ff=r.district_freeform or '(empty)', district=district, date=r.datetime.strftime('%d/%m/%Y %H:%M'), sender=r.connection.identity, names=r.names or '(empty)', currency=currency)

        return render_to_response('igreport/report-preview.html', dict(rpt=report), RequestContext(request))

    except Exception as err:
        return HttpResponse(err.__str__(), status=500)