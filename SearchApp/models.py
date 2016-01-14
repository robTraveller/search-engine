# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Remove `managed = False` lines if you wish to allow Django to create and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
#
# Also note: You'll have to insert the output of 'django-admin.py sqlcustom [appname]'
# into your database.
from __future__ import unicode_literals

from django.db import models

class t_user(models.Model):
	id = models.AutoField(primary_key=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_searched = models.DateTimeField(auto_now=True)
	top_path = models.CharField(max_length=100)
	user_id = models.CharField(max_length=20)
	has_more = models.BooleanField(False)
	class Meta:
		managed = False
		db_table = 'config'

class Documents(models.Model):
	id = models.AutoField(primary_key=True)
	date_created = models.DateTimeField(auto_now_add=True)
	date_searched = models.DateTimeField(auto_now=True)
	url = models.TextField()
	title = models.CharField(max_length=255)
	uid = models.CharField(max_length=20)
	level = models.IntegerField(default=0,null=True)
	error_code = models.IntegerField(default=0, null=False)
	raw_size = models.IntegerField(default=0, null=False)
	craw_size = models.IntegerField(default=0, null=False)
	standard_rate = models.DecimalField(max_digits=7, decimal_places=2, default = 0.5, null=False)
	status = models.IntegerField(default=0, null=False)
	error_msg = models.TextField()
	class Meta:
		managed = True
		db_table = 'resaddr'

# Article table
class Contents(models.Model):
	id = models.AutoField(primary_key=True)
	group_id = models.IntegerField()
	group_id2 = models.IntegerField()
	doc = models.ForeignKey('Documents')        # SearchTags table's ForeignKey
	paragraph = models.TextField()                  # The content
	tag = models.CharField(max_length=255)      # For example: <html><body><div><a>
	class Meta:
		managed = True
		db_table = 'contents'
	# def findLastGroupNumber(self):

	# def saveGroupContents(self, paras, tags):


class Tags(models.Model):
	docid = models.IntegerField()
	tagid = models.IntegerField()
	class Meta:
		managed = True
		db_table = 'tags'

