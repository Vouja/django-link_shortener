from django.urls import path
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
	path('', CreateLink.as_view(), name='create'),
	path('homepage/success/<str:link>', TemplateView.as_view(template_name='linker/created.html'), name='success'),
	path('homepage/fail/', TemplateView.as_view(template_name='linker/created_fail.html'), name='fail'),
	path('<str:link>/', RedirectAdress.as_view(), name='redirect'),
]
