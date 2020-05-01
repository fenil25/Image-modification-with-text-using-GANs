from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.db.models import Max

from app.models import Edit
from app.forms import EditForm, OldEditForm
from app import views
from gallery import settings

def bird_model(original, text):
	return original


def fashion_model(original, text):
	return original


def transform(request):
# Handle file upload
	if request.method == 'POST':
		print("Transform POST")
		form = EditForm(request.POST, request.FILES)
		if form.is_valid():
			dataset = request.POST['dataset']
			num_id = Edit.objects.filter(dataset = dataset).aggregate(Max('num_id')).get('num_id__max')
			if num_id == None:
				num_id = 1
			else:
				num_id += 1
			desc = request.POST['desc']
			original = request.FILES['original']

			if dataset == 'bird':
				result = bird_model(original, desc)
			else:
				result = fashion_model(original, desc)
			new_edit = Edit(num_id = num_id, dataset = dataset, desc = desc, original = original, result = result)
			new_edit.save()

			# Redirect to the document list after POST
			return HttpResponseRedirect(reverse(views.transform))
	else:
		print("Transform GET")
		form = EditForm()
		try:	
			last_edit = Edit.objects.latest('id')
			return render(request, 'app/form.html', {'last_edit': last_edit, 'form': form})
		except Exception as e:
			print(e)
			return render(request, 'app/form.html', {'form': form})


def transform_old(request, id, side):
	x = Edit.objects.get(id = id)
	field_object = Edit._meta.get_field(side)
	field_value = field_object.value_from_object(x)
	if request.method == 'POST':
		print("OLD POST")
		form = OldEditForm(request.POST)
		if form.is_valid():
			dataset = x.dataset
			num_id = Edit.objects.filter(dataset = dataset).aggregate(Max('num_id')).get('num_id__max')
			if num_id == None:
				num_id = 1
			else:
				num_id += 1
			desc = request.POST['desc']
			original = field_value
			if dataset == 'bird':
				result = bird_model(original, desc)
			else:
				result = fashion_model(original, desc)
			new_edit = Edit(num_id = num_id, dataset = dataset, desc = desc, original = original, result = result)
			new_edit.save()
			print('Old edit saved')
			return HttpResponseRedirect(reverse(views.transform))
	else:
		form = OldEditForm()
		img = field_value
		return render(request, 'app/old_edit.html', {'old': img, 'form': form, 'id': id, 'side': side})


def index(request):
	return render(request, 'app/index.html')


def list(request, dataset):
	return render(request, 'app/list.html', {'pairs': Edit.objects.filter(dataset = dataset).order_by('-num_id')})
