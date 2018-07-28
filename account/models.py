from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

def upload_location(instance,filename):
	return "%s/%s" %(instance.id,filename)

class Profile(models.Model):
	user=models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
	date_of_birth=models.DateField(blank=True,null=True)
	photo=models.ImageField(upload_to=upload_location,default='160Hf.png')

	def __str__(self):
		return 'Profile of {}'.format(self.user.username)

	def get_absolute_url(self):
		return reverse('user_detail',args=[self.user.username])


