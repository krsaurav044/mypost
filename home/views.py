from django.shortcuts import render,redirect
from images.models import Image
# Create your views here.

def homepage(request):
	
	return render(request,'home.html',{})