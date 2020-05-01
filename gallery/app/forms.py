from django import forms

class EditForm(forms.Form):
	dataset_choices = [('flower', 'flower'), ('bird', 'bird'), ('fashion', 'fashion')]
	original = forms.FileField(label = 'Select an image.')
	desc = forms.TextField()
	dataset = forms.ChoiceField(choices = dataset_choices)
