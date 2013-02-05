from django.shortcuts import render_to_response
from django.template import RequestContext
from igreport.models import Category
from rapidsms.contrib.locations.models import Location
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache

@login_required
@never_cache
def show_categories(request):
    return render_options(Category.objects.order_by('name'), request)

@login_required
def show_districts(request):
    return render_options(Location.objects.filter(type__name='district').order_by('name'), request)

@login_required
def show_subcounties(request):
    return render_options(Location.objects.filter(type__name='sub_county').order_by('name'), request)


def render_options(entities, request):
    return render_to_response(
    "igreport/options.html", { \
        'entities':entities,
    }, context_instance=RequestContext(request))
