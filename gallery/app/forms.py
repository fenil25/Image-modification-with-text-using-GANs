from django import forms
from string import Template
from django.utils.safestring import mark_safe
from gallery import settings

class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, renderer=None):
        html = Template("""<img src="$link"/>""")
        return mark_safe(html.substitute(media = settings.MEDIA_ROOT, link=value))

class EditForm(forms.Form):
	dataset_choices = [('flower', 'flower'), ('bird', 'bird'), ('fashion', 'fashion')]
	original = forms.ImageField(label = 'Select an image.',
		widget = forms.ClearableFileInput(attrs={'onchange': 'upload_img(this);'})
	)
	desc = forms.CharField()
	dataset = forms.ChoiceField(choices = dataset_choices)

class OldEditForm(forms.Form):
	desc = forms.CharField()
