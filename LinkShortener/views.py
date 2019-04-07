from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
import validators
from django.core.validators import URLValidator
from .generator import generate_short_link, format_link
from .session import request_checker
from django.http import Http404
import datetime
from django.contrib.sites.models import Site

#templates
link_create = 'linker/create.html'
link_created = 'linker/created.html'
link_created_fail = 'linker/created_fail.html'

link_error_404 = 'erros/error_404.html'

#homepage
class CreateLink(View):
	def get(self, request):
		form = LinkForm()
		return render(request, link_create, context={
			'form': form,
			'error': '',
		})
	def post(self, request):
		error = ''
		form = LinkForm(request.POST)
		if form.is_valid():
			linkb = form.cleaned_data['link']

			#validate a link
			linkb = format_link(linkb)
			validator = URLValidator()
			try:
				validator(linkb)
			except:
				error = 'incorrect link!'

			#check maximum amount of shorten links produced in a row
			error = request_checker(request, error)

			#not ok
			if error != '':
				return render(request, link_create, context={
					'form': form,
					'error': error,
				})

			#ok, save to db
			name = form.cleaned_data['name']
			links = generate_short_link(linkb, name)
			model = LinkModel(linkb=linkb, links=links)
			model.save()

			return redirect(reverse('success', args=(links,)))

		return render(request, link_create, context={
			'form': form,
			'error': '',
		})

#redirect by shorten link
class RedirectAdress(View):
	def get(self, request, link):
		group = get_object_or_404(LinkModel, links=link)
		return redirect(group.linkb)

#only successful can get here
class SuccessRedirect(View):
	def get(self, request, link):
		print(request.session.get('success'))
		if request.session.get('success'):
			request.session['success'] = False
			request.session.modified = True
			current_site = Site.objects.get_current()
			return render(request, link_created, context={
				'link': current_site.domain+'/'+link,
			})
		else:
			raise Http404

#only unsuccessful can get here
class FailRedirect(View):
	def get(self, request, link):
		print(request.session.get('fail'))
		if request.session.get('fail'):
			request.session['fail'] = False
			request.session.modified = True
			return render(request, link_created_fail, context={
				'link': link,
			})
		else:
			raise Http404

# def error_404(request, exception):
# 	return render(request, link_error_404)
