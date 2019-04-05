from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View
from .models import *
from .forms import *
from randomwordgenerator import randomwordgenerator
import datetime
from django.http import HttpResponseRedirect
import os
import validators
from django.core.validators import URLValidator


link_create = 'linker/create.html'
link_created = 'linker/created.html'
link_created_fail = 'linker/created_fail.html'

def generate_short_link(link, name):
	if name == '':
		name = randomwordgenerator.generate_random_words(1)
	now = datetime.datetime.now()
	return '{}{}{}{}'.format(name, now.strftime("%m"),  now.strftime("%d"), now.strftime("%M"), now.strftime("%S"))


class CreateLink(View):
	def get(self, request):
		form = LinkForm()
		return render(request, link_create, context={
			'form': form,
		})
	def post(self, request):
		form = LinkForm(request.POST)
		if form.is_valid():
			linkb = form.cleaned_data['link']
			
			if linkb[:7] != 'http://' and linkb[:8] != 'https://':
				linkb = 'http://{}'.format(linkb)

			validator = URLValidator()
			try:
				validator(linkb)
			except:
				print(linkb)
				return render(request, link_create, context={
					'form': form,
				})
			name = form.cleaned_data['name']
			links = generate_short_link(linkb, name)
			model = LinkModel(linkb=linkb, links=links)
			model.save()
			return redirect(reverse('success', args=(links,)))

		return render(request, link_create, context={
			'form': form,
		})

class RedirectAdress(View):
	def get(self, request, link):
		group = get_object_or_404(LinkModel, links=link)
		print(group.linkb)
		return redirect(group.linkb)
