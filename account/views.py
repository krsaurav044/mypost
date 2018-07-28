from django.shortcuts import render,get_object_or_404,redirect
from .forms import LoginForm,RegistrationForm,UserEditForm,ProfileEditForm
from django.http import HttpResponse
from django.contrib.auth import authenticate,login
from .models import Profile
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from images.models import Image
from actions.utils import create_action
# Create your views here.

def login_view(request):
	if request.method=='POST':
		form=LoginForm(request.POST)
		if form.is_valid():
			cd=form.cleaned_data
			user=authenticate(username=cd['username'],password=cd['password'])
			if user is not None:
				if user.is_active:
					login(request,user)
					request.session['member_id'] = user.id
					return redirect('images:list',username=user.username)
				else:
					return HttpResponse('Disabled account')
			else:
				return HttpResponse('Invalid account')
	else:
		form=LoginForm()
		return render(request,'login.html',{'form':form})

def register(request):
	if request.method=='POST':
		user_form=RegistrationForm(request.POST)
		if user_form.is_valid():
			new_user=user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()
			# Create the user profile
			profile = Profile.objects.create(user=new_user)
			#create_action(new_user,'has created an account')
			return render(request,'register_done.html',{'new_user':new_user})

	else:
		user_form=RegistrationForm()
	return render(request,'register.html',{'user_form':user_form})


@login_required
def edit(request,username):
	user=get_object_or_404(User,username=username)
	if request.method=='POST':
		user_form=UserEditForm(instance=request.user,data=request.POST)
		profile_form=ProfileEditForm(request.POST,request.FILES,instance=request.user.profile)
		if user_form.is_valid() and profile_form.is_valid():
			user_form.save()
			new_item=profile_form.save(commit=False)
			profile_form.save()
			create_action(request.user,'Updated his  profile',new_item)
			messages.success(request,'Profile updated successfully')
			return redirect('user_detail',username=user.username)
		else:
			messages.error(request,'Error in updating your profile')
	else:
		user_form=UserEditForm(instance=request.user)
		profile_form=ProfileEditForm(instance=request.user.profile)
	return render(request,'edit.html',{'user_form': user_form,'profile_form': profile_form})


@login_required
def user_list(request):
	users=User.objects.filter(is_active=True)
	images=Image.objects.all()
	return render(request,'list.html',{'users':users,'images':images})


@login_required
def user_detail(request,username):
	user=get_object_or_404(User,username=username,is_active=True)
	return render(request,'detail.html',{'section':'people','user':user})


@login_required
def profile_view(request,username):

	user=get_object_or_404(User,username=username)
	return render(request,'profile.html',{'user':user})

def logout_view(request):
	try:
		del request.session['member_id']
	except KeyError:
		pass
	return redirect('logout')