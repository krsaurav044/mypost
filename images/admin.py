from django.contrib import admin
from .models import Image
from django.contrib.sessions.models import Session
# Register your models here.
class ImageAdmin(admin.ModelAdmin):
	list_display=('title','slug','image','created')
	list_filter=['created']
class SessionAdmin(admin.ModelAdmin):
	def _session_data(self, obj):
		return obj.get_decoded()
	list_display = ['session_key', '_session_data', 'expire_date']

admin.site.register(Image,ImageAdmin)
#admin.site.register(Comment)
admin.site.register(Session,SessionAdmin)