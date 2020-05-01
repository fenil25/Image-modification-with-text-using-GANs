from django.db import models

# Create your models here.

def file_directory_path(instance, file_name):
	# Returns a file path in the form MEDIA_ROOT/<type>/<num_id>/

class Edit(models.Model):
	num_id = models.IntegerField()
	dataset = models.CharField()  # flower/bird/fashion
	original = models.FileField(upload_to = '{0}/{1}/original.jpg'.format(self.dataset, self.num_id))
	desc = models.TextField()
	result = models.FileField(upload_to = '{0}/{1}/result.jpg'.format(self.dataset, self.num_id))
