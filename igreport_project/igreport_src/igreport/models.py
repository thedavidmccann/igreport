#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8

from django.db import models
from django.contrib.auth.models import User
from rapidsms.models import Connection
from rapidsms.contrib.locations.models import Location
from script.signals import script_progress_was_completed
from .signal_handlers import handle_report

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    district = models.ForeignKey(Location, null=True, default=None)

class Category(models.Model):
    name = models.TextField()
    description = models.TextField()

class Comment(models.Model):
    report = models.ForeignKey('IGReport', related_name='comments')
    user = models.ForeignKey(User, null=True, default=None)
    datetime = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

class IGReport(models.Model):
    connection = models.ForeignKey(Connection)
    completed = models.BooleanField(default=False)
    synced = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True)
    report = models.TextField()
    name = models.TextField(blank=True, null=True, default=None)
    district = models.ForeignKey(Location, null=True, default=None, related_name='district_reports')
    subcounty_freeform = models.TextField(blank=True, null=True, default=None)
    subcounty = models.ForeignKey(Location, null=True, default=None, related_name='subcounty_reports')
    when_freeform = models.TextField(null=True, blank=True)
    when_datetime = models.DateTimeField(default=None, null=True)
    category = models.ForeignKey(Category, null=True, default=None)

script_progress_was_completed.connect(handle_report, weak=False)
