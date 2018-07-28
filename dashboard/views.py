from django.shortcuts import render,get_object_or_404

# Create your views here.
from django.contrib.auth.models import User
from friendship.models import Friend, Follow, Block
from images.models import Image



def homepage(request,username):
	user = get_object_or_404(User, username=username)
	friendss=Friend.objects.friends(request.user)
	images=Image.objects.all()
	return render(request,'home2.html',{'images':images,'friendss':friendss})