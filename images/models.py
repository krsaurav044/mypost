from django.db import models
from django.urls import reverse
from django.contrib.contenttypes.models import ContentType
from django.conf import settings
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.auth.models import User
from actions.models import Action
# Create your models here.
def upload_location(instance,filename):
	return "%s/%s" %(instance.id,filename)
class Image(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,related_name='images_created',on_delete=models.CASCADE)
	title=models.CharField(max_length=200)
	slug=models.SlugField(max_length=200,blank=True)
	image=models.ImageField(upload_to=upload_location)
	description=models.TextField(blank=True)
	created=models.DateField(auto_now_add=True,db_index=True)
	user_like=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='images_liked',blank=True)
	total_likes=models.PositiveIntegerField(db_index=True,default=0)
	

	def __str__(self):
		return self.title

	def save(self,*args,**kwargs):
		if not self.slug:
			self.slug=slugify(self.title)
			super(Image,self).save(*args,**kwargs)
	def get_absolute_url(self):
		return reverse('images:detail',args=[self.id])

	def get_like_url(self):
		return reverse('images:like-toggle',args=[self.id])
	def get_like_url1(self):
		return reverse('images:like-toggle1',args=[self.id])
	def get_absolute_url1(self):
		return reverse('images:list',args=[self.user.username])

	@property
	def get_content_type(self):
		instance=self
		content_type=ContentType.objects.get_for_model(instance.__class__)
		return content_type
	










