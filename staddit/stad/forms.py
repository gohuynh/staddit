from django import forms
from django.forms import ModelForm
from stad import models

class postedByForm(forms.Form):
	class Meta:
		model  = models.Posted_By
		fields = ['author', 'id']


class subredditForm(forms.Form):
	subreddit = forms.CharField(label = 'sub', max_length = 25)

	def clean_sub(self):
		sub = self.cleaned_data.get('subreddit')
		if len(sub) < 3 or len(sub) > 26:
			raise forms.ValidationError("Please enter a valid subreddit")
		return sub


class redditorForm(forms.Form):
	author = forms.CharField(label = 'redditor', max_length = 25)

	def clean_sub(self):
		auth = self.cleaned_data.get('author')
		if len(auth) < 3 or len(auth) > 26:
			raise forms.ValidationError("Please enter a valid Redditor")
		return auth