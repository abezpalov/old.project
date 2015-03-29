from django.db import models
from django.utils import timezone

# Category
class Category(models.Model):
	name        = models.CharField(max_length=100)
	alias       = models.CharField(max_length=100)
	description = models.TextField()
	parent      = models.ForeignKey('self', null=True, default=None)
	level       = models.IntegerField()
	order       = models.IntegerField()
	path        = models.CharField(max_length=512, null=True)
	state       = models.BooleanField(default=True)
	created     = models.DateTimeField()
	modified    = models.DateTimeField()

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['order']

# Doc Type
class DocType(models.Model):
	name     = models.CharField(max_length=100)
	alias    = models.CharField(max_length=100)
	state    = models.BooleanField(default=True)
	created  = models.DateTimeField()
	modified = models.DateTimeField()

	def __str__(self):
		return self.alias

	class Meta:
		ordering = ['alias']

# Language
class Language(models.Model):
	name     = models.CharField(max_length=100)
	alias    = models.CharField(max_length=100)
	state    = models.BooleanField(default=True)
	created  = models.DateTimeField()
	modified = models.DateTimeField()

	def __str__(self):
		return self.alias

	class Meta:
		ordering = ['alias']

# Content
class Content(models.Model):
	title        = models.CharField(max_length=100)
	alias        = models.CharField(max_length=100, null=True)
	patch        = models.CharField(max_length=512, null=True)
	src          = models.CharField(max_length=512, null=True)
	thumb_src    = models.CharField(max_length=512, null=True)
	doc_type     = models.ForeignKey(DocType, null=True, default=None)

	intro        = models.TextField()
	content      = models.TextField()
	description  = models.TextField()
	banner_main  = models.TextField()
	banner_side  = models.TextField()

	category     = models.ForeignKey(Category, null=True, default=None)
	language     = models.ForeignKey(Language, null=True, default=None)

	source       = models.CharField(max_length=512, null=True)
	source_url   = models.CharField(max_length=512, null=True)

	state        = models.BooleanField(default=True)
	pub_from     = models.DateTimeField()
	pub_to       = models.DateTimeField()

	on_main      = models.BooleanField(default=False)
	on_side      = models.BooleanField(default=False)
	on_news      = models.BooleanField(default=False)
	power        = models.IntegerField(default=1)

	created      = models.DateTimeField()
	created_by   = models.CharField(max_length=100)
	modified     = models.DateTimeField()
	modified_by  = models.CharField(max_length=100)
	published    = models.DateTimeField(null=True, default=None)
	published_by = models.CharField(max_length=100)
	pub_from     = models.DateTimeField(null=True, default=None)
	pub_to       = models.DateTimeField(null=True, default=None)

	def __str__(self):
		return self.title
