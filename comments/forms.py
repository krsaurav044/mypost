from django import forms

class ComentForm(forms.Form):
	content_type=forms.CharField(widget=forms.HiddenInput)
	object_id=forms.IntegerField(widget=forms.HiddenInput)
	content=forms.CharField(max_length=400)
