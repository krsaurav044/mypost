from django.conf.urls import url
from . import views
from django.contrib.auth import views as auth_views

urlpatterns=[
      url(r'login/$',views.login_view,name='login'),
      url(r'register/$',views.register,name='register'),
      url(r'edit/(?P<username>[-\w]+)/$',views.edit,name='edit'),
      url(r'users/$',views.user_list,name='list'),
      
     url(r'^users/(?P<username>[-\w]+)/$',views.user_detail,name='user_detail'),
     url(r'logout/$',auth_views.logout,name='logout'),
     url(r'^profile/(?P<username>[-\w]+)/$',views.profile_view,name='profile'),
      url(r'log-out/$',views.logout_view,name='log-out'),

]