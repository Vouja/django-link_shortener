from django.db import models

#save origin link and short one
class LinkModel(models.Model):
	linkb = models.CharField(max_length=200)
	links = models.CharField(max_length=200, unique=True)
	time = models.DateTimeField(auto_now=True)

	class Meta:
		ordering = ('time',)
