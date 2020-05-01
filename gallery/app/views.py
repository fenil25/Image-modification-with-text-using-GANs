from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.db.models import Max

from gallery.app.models import Edit
from gallery.app.forms import EditForm

def bird_model(original, text):
	return original

def fashion_model(original, text):
	return original

def list(request):
    # Handle file upload
    if request.method == 'POST':
        form = EditForm(request.POST, request.FILES)
        if form.is_valid():
        	# Call your model here
        	num_id = Edit.objects.aggregate(Max('num_id')) + 1
        	dataset = request.POST['dataset']
        	desc = request.POST['desc']
        	original = request.FILES['original']
        	
        	if dataset == 'bird':
        		result = bird_model(original, text)
        	else:
        		result = fashion_model(original, text)

            new_edit = Edit(num_id = num_id, dataset = dataset, desc = desc, original = original, result = result)
            new_edit.save()

            # Redirect to the document list after POST
            return HttpResponseRedirect(reverse('gallery.app.views.list'))
    else:
        form = EditForm() # A empty, unbound form

    # Load documents for the list page
    pairs = Edit.objects.all()

    # Render list page with the documents and the form
    return render_to_response(
        'myapp/list.html',
        {'pairs': pairs, 'form': form},
        context_instance=RequestContext(request)
    )

def index(request):
    return render_to_response('myapp/index.html')
