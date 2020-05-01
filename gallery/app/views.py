from django.shortcuts import render
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.urls import reverse

from django.db.models import Max

from app.models import Edit
from app.forms import EditForm
from app import views

def bird_model(original, text):
	return original

def fashion_model(original, text):
	return original

# def list(request):
# # Handle file upload
# 	if request.method == 'POST':
# 		form = EditForm(request.POST, request.FILES)
# 		if form.is_valid():
# 			# Call your model here
# 			num_id = Edit.objects.aggregate(Max('num_id')).get('num_id__max')
# 			if num_id == None:
# 				num_id = 1
# 			else:
# 				num_id += 1
# 			dataset = request.POST['dataset']
# 			desc = request.POST['desc']
# 			original = request.FILES['original']

# 			if dataset == 'bird':
# 				result = bird_model(original, desc)
# 			else:
# 				result = fashion_model(original, desc)
# 			new_edit = Edit(num_id = num_id, dataset = dataset, desc = desc, original = original, result = result)
# 			new_edit.save()

# 			# Redirect to the document list after POST
# 			return HttpResponseRedirect(reverse(views.list))
# 	else:
# 		form = EditForm() # A empty, unbound form

# 	# Load documents for the list page
# 	pairs = Edit.objects.all()

# 	# Render list page with the documents and the form
# 	return render(
# 		request, 
# 		'app/list.html',
# 		{'pairs': pairs, 'form': form},
# 	)


def index(request):
	return render(request, 'app/index.html')


def list(request, dataset):
	return render(request, 'app/list.html', {'pairs': Edit.objects.filter(dataset = dataset).order_by('-num_id')})
