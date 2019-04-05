from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import View
from .models import *
from .forms import *
from django.http import HttpResponseRedirect
import validators
from django.core.validators import URLValidator
from .generator import generate_short_link, format_link
from django.http import Http404
import datetime

MAX_NUM = 3

link_create = 'linker/create.html'
link_created = 'linker/created.html'
link_created_fail = 'linker/created_fail.html'


class CreateLink(View):
	def get(self, request):
		form = LinkForm()
		return render(request, link_create, context={
			'form': form,
			'error': '',
		})
	def post(self, request):
		form = LinkForm(request.POST)
		if form.is_valid():
			linkb = form.cleaned_data['link']

			linkb = format_link(linkb)
			validator = URLValidator()
			try:
				validator(linkb)
			except:
				print(linkb)
				return render(request, link_create, context={
					'form': form,
					'error': 'incorrect link!',
				})

			name = form.cleaned_data['name']
			links = generate_short_link(linkb, name)
			print(links)
			model = LinkModel(linkb=linkb, links=links)

			if not request.session.get('used'):
				request.session['used'] = 0

			if request.session.get('used')>MAX_NUM:
				time = datetime.datetime.now().strftime("%H")
				if int(request.session.get('time')) - int(time) >0:
					request.sesson['used'] = 0
				else:
					return render(request, link_create, context={
						'form': form,
						'error': 'wait a bit!',
					})

			request.session['used'] = request.session['used']+1
			request.session['time'] = datetime.datetime.now().strftime("%H")
			request.session['success'] = True
			request.session.modified = True

			model.save()

			return redirect(reverse('success', args=(links,)))

		return render(request, link_create, context={
			'form': form,
			'error': '',
		})

class RedirectAdress(View):
	def get(self, request, link):
		group = get_object_or_404(LinkModel, links=link)
		return redirect(group.linkb)

class SuccessRedirect(View):
	def get(self, request, link):
		print(request.session.get('success'))
		if request.session.get('success'):
			request.session['success'] = False
			request.session.modified = True
			return render(request, 'linker/created.html', context={
				'link': link,
			})
		else:
			raise Http404

class FailRedirect(View):
	def get(self, request, link):
		print(request.session.get('fail'))
		if request.session.get('fail'):
			request.session['fail'] = False
			request.session.modified = True
			return render(request, 'linker/created_fail.html', context={
				'link': link,
			})
		else:
			raise Http404
