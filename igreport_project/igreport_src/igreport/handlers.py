#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4 encoding=utf-8

from piston.handler import BaseHandler
from piston.utils import validate
from .models import IGReport
from .forms import IGReportForm

class IGReportHandler(BaseHandler):
    allowed_methods = ('GET', 'POST')
    model = IGReport
    fields = ('id', 'report', 'subject', 'district', 'subcounty_freeform', 'subcounty', 'datetime', 'when_freeform', 'when_datetime')

    def read(self, request, figure_id=None):
        base = IGReport.objects

        if figure_id:
            return base.get(pk=figure_id)
        else:
            return base.all()

    @validate(IGReportForm)
    def create(self, request):
        figure = IGReport.objects.create(
#            primitive_type=request.POST.get('primitive_type'),
#            short_description=request.POST.get('short_description'),
#            description=request.POST.get('description'),
        )
        return figure
