from django.db import models

# Create your models here.

def orig_file_directory_path(instance, file_name):
	# Returns a file path in the form MEDIA_ROOT/<type>/<num_id>/
	return '{0}/{1}/{2}'.format(instance.dataset, instance.num_id, file_name)

def result_file_directory_path(instance, file_name):
	# Returns a file path in the form MEDIA_ROOT/<type>/<num_id>/
	return '{0}/{1}/{2}'.format(instance.dataset, instance.num_id, file_name)

class Edit(models.Model):
	dataset_choices = [('flower', 'flower'), ('bird', 'bird'), ('fashion', 'fashion')]
	num_id = models.IntegerField()
	dataset = models.CharField(choices = dataset_choices, max_length = 10)  # flower/bird/fashion
	original = models.ImageField(upload_to = orig_file_directory_path)
	desc = models.TextField()
	result = models.ImageField(upload_to = result_file_directory_path)
