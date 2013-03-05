#!/usr/bin/env python
# vim: ai ts=4 sts=4 et sw=4
# encoding=utf-8

from django.db import models
from django.contrib.auth.models import User
from rapidsms.models import Connection
from rapidsms.contrib.locations.models import Location
from script.signals import script_progress_was_completed
from .signal_handlers import handle_report, igreport_pre_save
from django.db.models.signals import pre_save
from rapidsms_httprouter.models import Message

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    district = models.ForeignKey(Location, null=True, default=None)

    class Meta:
        verbose_name = 'User Profile'
        verbose_name_plural = 'User Profiles'

class Category(models.Model):
    name = models.TextField()
    description = models.TextField()

    class Meta:
        verbose_name = 'Report Category'
        verbose_name_plural = 'Report Categories'

class Comment(models.Model):
    report = models.ForeignKey('IGReport', related_name='comments')
    user = models.ForeignKey(User, null=True, default=None)
    datetime = models.DateTimeField(auto_now_add=True)
    comment = models.TextField()

class IGReport(models.Model):
    connection = models.ForeignKey(Connection)
    completed = models.BooleanField(default=False)
    synced = models.BooleanField(default=False)
    datetime = models.DateTimeField(auto_now_add=True, verbose_name='Report Date')
    keyword = models.TextField(blank=True, null=True, default=None)
    report = models.TextField()
    subject = models.TextField(blank=True, null=True, default=None)
    district = models.ForeignKey(Location, null=True, default=None, related_name='district_reports')
    categories = models.ManyToManyField(Category, related_name='reports')
    amount_freeform = models.TextField(null=True, blank=True)
    amount = models.DecimalField(decimal_places=2, max_digits=26, null=True)
    names = models.TextField(null=True, blank=True)

    @property
    def reference_number(self):
        return "SMS/%d/%d/%d" % (self.id, self.datetime.month, self.datetime.year)

    class Meta:
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'

class Unprocessed(Message):
    class Meta:
        proxy = True
        verbose_name = 'Unprocessed Message'
        verbose_name_plural = 'Unprocessed Messages'

script_progress_was_completed.connect(handle_report, weak=False)
pre_save.connect(igreport_pre_save, sender=IGReport, weak=False)
