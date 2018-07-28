from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from .forms import ImageCreateForm
from comments.forms import ComentForm
from .models import Image
from django.http import JsonResponse,HttpResponse
from friendship.models import Friend, Follow, Block
from images.models import Image
from django.contrib.auth.models import User
from comments.models import Coment
from actions.utils import create_action
from actions.models import Action
from django.contrib.sessions.models import Session
from django.utils import timezone
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from common.decorators import ajax_required
from django.views.decorators.http import require_POST
from django.views.generic import RedirectView
#from common.decorators import ajax_required
#from django.views.decorators.http import require_POST
#from actions.utils import create_action
# Create your views here.

@login_required
def image_create(request):
	if request.method=='POST':
		form=ImageCreateForm(request.POST,request.FILES)
		if form.is_valid():
			cd=form.cleaned_data
			new_item=form.save(commit=False)
			new_item.user=request.user
			new_item.save()
			create_action(request.user,'Posted an image',new_item)
			messages.success(request,'Image added successfully')
			return redirect('image:detail',id=new_item.id)

	else:
		form=ImageCreateForm(data=request.GET)
	return render(request,'images/image/create.html',{'form':form})
	
@login_required
def image_list(request,username):
	images=Image.objects.all()
	user=get_object_or_404(User,username=username)
	active_sessions=Session.objects.filter(expire_date__gte=timezone.now())
	user_id_list=[]
	for session in active_sessions:
		data=session.get_decoded()
		user_id_list.append(data.get('_auth_user_id',None))
	


	friendss=Friend.objects.friends(request.user)
	friendss_ids = [friend.id for friend in friendss]
	online_friends=User.objects.filter(id__in=user_id_list).filter(id__in=friendss_ids)
	#online_friends=online_users.filter(id__in=friendss_ids)
	actions=Action.objects.filter(user_id__in=friendss_ids).select_related('user')
	query=request.GET.get("q")
	if query:
		actions=actions.filter(user__username=query)
	paginator = Paginator(actions, 20) # Show 25 contacts per page
	page = request.GET.get('page')
	actions = paginator.get_page(page)
	#if friendss:
		#actions=actions.filter(user_id__in=friend_ids).select_related('user','user__profile').prefetch_related('target')
		#actions=actions[:10]
	return render(request,'images/image/img_list.html',{'friendss':friendss,'actions':actions,
		                                                'images':images,'online_friends':online_friends})


def image_detail(request, id):
	image = get_object_or_404(Image, id=id)
	#content_type=ContentType.objects.get_for_model(Image)
	#obj_id=image.id
	initial_data={
	      "content_type":image.get_content_type,
	      "object_id":image.id
	}
	form=ComentForm(request.POST or None,initial=initial_data)
	if form.is_valid():
		c_type=form.cleaned_data.get("content_type")
		content_type=ContentType.objects.get(model=c_type)
		obj_id=form.cleaned_data.get('object_id')
		content_data=form.cleaned_data.get("content")
		new_comment, created=Coment.objects.get_or_create(
			                                    user=request.user,
			                                    content_type=content_type,
			                                    object_id=obj_id,
			                                    content=content_data
			                                  )
		create_action(request.user,'Commented ',image)
		
	comments=Coment.objects.filter_by_instance(image)
	return render(request,'images/image/detail.html',{'section': 'images','comment_form':form,'comments':comments,'image': image})


class PostLikeToggle(RedirectView):
	def get_redirect_url(self,*arg,**kwargs):
		id=self.kwargs.get("id")
		print(id)
		obj=get_object_or_404(Image,id=id)
		url_=obj.get_absolute_url()
		user=self.request.user
		if user in obj.user_like.all():
			obj.user_like.remove(user)
		else:
			obj.user_like.add(user)
		return url_

class PostLikeToggle1(RedirectView):
	def get_redirect_url(self,*arg,**kwargs):
		id=self.kwargs.get("id")
		print(id)
		obj=get_object_or_404(Image,id=id)
		url_=obj.get_absolute_url1()
		user=self.request.user
		if user in obj.user_like.all():
			obj.user_like.remove(user)
		else:
			obj.user_like.add(user)
		return url_