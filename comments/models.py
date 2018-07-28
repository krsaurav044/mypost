from django.db import models
from django.conf import settings
from images.models import Image
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
# Create your models here.

class ComentManager(models.Manager):
	def filter_by_instance(self,instance):
		content_type=ContentType.objects.get_for_model(Image)
		obj_id=instance.id
		qs=super(ComentManager,self).filter(content_type=content_type,object_id=obj_id)
		return qs

class Coment(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1,on_delete=models.CASCADE)
	#post=models.ForeignKey(Image,on_delete=models.CASCADE)
	content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
	object_id = models.PositiveIntegerField()
	content_object = GenericForeignKey('content_type', 'object_id')
	content=models.TextField()
	created=models.DateTimeField(auto_now_add=True)

	objects=ComentManager()

	def __str__(self):
		return self.user.username

	class Meta:
		ordering=('-created',)
