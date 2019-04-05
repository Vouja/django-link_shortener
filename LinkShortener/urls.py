from django.urls import path
from .views import *
from django.views.generic import TemplateView

urlpatterns = [
	path('', CreateLink.as_view(), name='create'),
	path('homepage/success/<str:link>', SuccessRedirect.as_view(), name='success'),
	path('homepage/fail/', FailRedirect.as_view(), name='fail'),
	path('<str:link>/', RedirectAdress.as_view(), name='redirect'),
]
