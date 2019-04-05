from django import forms


class LinkForm(forms.Form):
	link = forms.CharField(max_length=200, required=True)
	name = forms.CharField(max_length=10, required=False)
