from django.db import models
from django.contrib.admin.models import User
from datetime import date

class Entity(models.Model):
	name = models.CharField(max_length=200)
	gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('N', 'N/A')])
	ent_type = models.CharField(max_length=1, choices=[('P', 'Individual'), ('I', 'Institution')], default='P')
	class Meta:
		verbose_name_plural = 'Entities'
		ordering = ['name']
	def __unicode__(self):
		return self.name

class ComplaintSource(models.Model):
	name = models.CharField(max_length=200)
	class Meta:
		verbose_name_plural = 'Complaint Sources'
		ordering = ['name']
	def __unicode__(self):
		return self.name

class Offence(models.Model):
	name = models.TextField()
	description = models.TextField()
	class Meta:
		verbose_name_plural = 'Offences'
		ordering = ['name']
	def __unicode__(self):
		return self.name

class District(models.Model):
	name = models.CharField(max_length=50, unique=True)
	description = models.TextField(blank=True)
	class Meta:
		verbose_name_plural = 'Districts'
		ordering = ['name']
	def __unicode__(self):
		return self.name

class Complaint(models.Model):
	statuses = (
		('US', 'unsubmitted'), ('OP', 'open'), ('OG', 'on going'), ('WL', 'with legal'), ('CL', 'closed'), ('AR', 'archived'),
	)

	complaint_reference = models.CharField(max_length=20, editable=False)
	complaint_no = models.IntegerField(blank=True, null=True, editable=False)
	registered_by = models.ForeignKey(User, related_name='registered_set', null=True)
	case_officer = models.ForeignKey(User, null=True, blank=True)
	source_of_complaint = models.ForeignKey(ComplaintSource, null=True)
	complainant = models.ForeignKey(Entity)
	accused = models.ForeignKey(Entity, related_name='accused_person')
	offences = models.ManyToManyField(Offence, null=True, blank=True)
	district = models.ForeignKey(District, null=True, default=None)
	status = models.CharField(max_length=2, choices=statuses)
	created_at = models.DateTimeField(auto_now_add=True)

	report = models.TextField()  # Updates

	def save(self, *args, **kwargs):
		if self.complaint_no:
			super(Complaint, self).save(*args, **kwargs)
			return

		today = date.today()
		time_ext = '%s/%s' % (today.month, today.year)
		complaint_num = 0
		try:
			last_c_num = max(Complaint.objects.filter(created_at__year=today.year,
			created_at__month=today.month, complaint_reference__icontains='SMS'
			).values_list('complaint_no', flat=True))
			if last_c_num > complaint_num:
				complaint_num = last_c_num
		except ValueError:
			pass

		self.complaint_no = complaint_num + 1
		self.complaint_reference = '%s/%s/%s' % ('SMS', self.complaint_no, time_ext)
		super(Complaint, self).save(*args, **kwargs)
	def __unicode__(self):
		return self.complaint_reference
	class Meta:
		db_table = 'complaints'

class Update(models.Model):
	staff = models.ForeignKey(User)
	complaint = models.ForeignKey(Complaint)
	attachment = models.FileField(upload_to='uploads/attachments/', max_length=250, blank=True)
	comment = models.TextField()
	created_at = models.DateTimeField(auto_now_add=True)  # auto_now_add=True Date fields should be unrestricted when making date transfers
	updated_at = models.DateTimeField(auto_now=True)
	class Meta:
		verbose_name_plural = 'Updates'
	def __unicode__(self):
		return self.complaint.complaint_reference
