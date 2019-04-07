from django import forms


class LinkForm(forms.Form):
	link = forms.CharField(max_length=200, required=True, widget=forms.TextInput)
	name = forms.CharField(max_length=10, required=False)

	link.widget.attrs.update({'class': 'input'})
	name.widget.attrs.update({'class': 'input'})
