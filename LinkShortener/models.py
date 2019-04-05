from django.db import models

#save origin link and short one
class LinkModel(models.Model):
	linkb = models.CharField(max_length=200) #original
	links = models.CharField(max_length=200, unique=True) #shorten
	time = models.DateTimeField(auto_now=True) #creation time

	class Meta:
		ordering = ('time',)
