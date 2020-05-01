from django.db import models

# Create your models here.

def file_directory_path(instance, file_name):
	# Returns a file path in the form MEDIA_ROOT/<type>/<num_id>/
	return None

class Edit(models.Model):
	dataset_choices = [('flower', 'flower'), ('bird', 'bird'), ('fashion', 'fashion')]
	num_id = models.IntegerField()
	dataset = models.CharField(choices = dataset_choices)  # flower/bird/fashion
	original = models.FileField(upload_to = '{0}/{1}/original.jpg'.format(dataset, num_id))
	desc = models.TextField()
	result = models.FileField(upload_to = '{0}/{1}/result.jpg'.format(dataset, num_id))
