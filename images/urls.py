from django.conf.urls import url
from . import views
from .views import PostLikeToggle,PostLikeToggle1

app_name='images'
urlpatterns = [
      url(r'^create/$', views.image_create, name='create'),
      url(r'^(?P<username>[\w-]+)/$', views.image_list, name='list'),
      #url(r'^comment/$', views.comment_view, name='comment'),
      url(r'^detail/(?P<id>\d+)/$',views.image_detail, name='detail'),
      url(r'^(?P<id>\d+)/like/$', PostLikeToggle.as_view(), name='like-toggle'),
       #url(r'^comment/(?P<id>[0-9]+)/$', views.add_comment, name='add_comment'),
       url(r'^(?P<id>\d+)/like1/$', PostLikeToggle1.as_view(), name='like-toggle1'),
      ]