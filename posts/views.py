from django.shortcuts import render
from posts.models import *
from . import forms 
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from posts.models import Like
from friendship.models import Friend
from django.db.models import Q 

@login_required
def home(request):
    p = Friend.objects.friends(user=User.objects.get(username=request.user.username))
    post_list = Posts.objects.filter(Q(user__in=p)|Q(user=request.user)).order_by('-time')
    page = request.GET.get('page', 1)

    paginator = Paginator(post_list, 5)

    try:
        postx = paginator.page(page)
    except PageNotAnInteger:
        postx = paginator.page(1)
    except EmptyPage:
        postx = paginator.page(paginator.num_pages)
  

    post_creation = forms.PostsForm()
    if request.method == "POST":
        post_creation = forms.PostsForm(request.POST,request.FILES)
        
        if post_creation.is_valid(): 
            entry = post_creation.save(commit=False)
            entry.user = request.user         
            entry.save()
            return HttpResponseRedirect(reverse('posts:home'))
    

    try:
        comment_field = forms.CommentForm()
        if request.method == "POST":
            comment_field = forms.CommentForm(request.POST)
            
            if comment_field.is_valid():
                comment_new = comment_field.save(commit=False)
                post_id = int(list(request.POST)[2])
                comment_new.post = get_object_or_404(Posts,pk=post_id)
                comment_new.userid = get_object_or_404(User,username=request.user.username)
                comment_new.save()

                return HttpResponseRedirect(reverse('posts:home'))
    except:
        pass
        
    return render(request,"posts/index.html",context={"postx":postx,
                            "user":post_creation,
                          "comment_field":comment_field,},
                          )


@login_required
def delete_post(request,post_id):
    post=Posts.objects.get(id=post_id)
    post.delete()
    return HttpResponseRedirect(reverse('posts:home')) 

@login_required
def delete_comment(request,comment_id,post_id):
    comments = Comment.objects.filter(post=Posts.objects.get(id=post_id))
    comments.filter(id=comment_id).delete()
    return HttpResponseRedirect(reverse('posts:home')) 

@login_required
def like(request,post_id):
    
    post=Posts.objects.get(id=post_id)
    like_obj = Like.objects.get_or_create(post=post,liked_by=request.user)[0]
    like_obj.save()
    return HttpResponseRedirect(reverse('posts:home')) 

@login_required
def dislike(request,post_id):

    post=Posts.objects.get(id=post_id)
    Like.objects.get(post=post,liked_by=request.user).delete()
    return HttpResponseRedirect(reverse('posts:home')) 

@login_required
def editpost(request,post_id):
    post=Posts.objects.get(id=post_id)
    if request.method == "POST":    
        post.post_text = request.POST.get('post_text')
        post.save()
        return HttpResponseRedirect(reverse('posts:home')) 

    return render(request,"posts/editpost.html",context={
                            "post_text":post.post_text,
                            },) 



#Alternative for form
        # name = request.POST.get('name')
        # time = timezone.now()
        # post_text = request.POST.get('post_text')

        # temp = Posts(name=name,time=time,post_text=post_text)
        # temp.save()