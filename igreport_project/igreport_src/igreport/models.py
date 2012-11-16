#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8

from django.db import models
from rapidsms.models import Connection
from rapidsms.contrib.locations.models import Location

class IGReport(models.Model):
    connection = models.ForeignKey(Connection)
    completed = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_add_now=True)
    report = models.TextField()
    name = models.CharField()
    location = models.ForeignKey(Location)

