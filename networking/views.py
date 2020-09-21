from django.shortcuts import render
from networking.models import *
from project_management.models import ProjectCreation,ProjectInductionRequest,ProjectMembers
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import User
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.db.models import Q
from project_colab import settings
from friendship.models import FriendshipRequest,Block,Follow,Friend
import os
import re

@login_required
def search(request):
    query = request.GET.get('q')
    query_type = request.GET['d']
    if query_type=="People":    
        u = User.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query) | Q(username__icontains=query)).exclude(username=request.user)
        return render(request,"networking/search.html",context={"user_list":u})

    elif query_type=="Project":

        word_lst = re.split('[, ]',query)
        query = Q()
        for word in word_lst:
            query = query | Q(tags__name__icontains=word) | Q(title__icontains=word)
        u = ProjectCreation.objects.filter(query).exclude(team_lead=request.user)
        return render(request,"networking/search.html",context={"project_list":u})
    

@login_required
def profile(request,username):
    u = User.objects.get(username=username)

    def check_relation(username):
        
        requested = len(FriendshipRequest.objects.filter(from_user=request.user,to_user=User.objects.get(username=username)))
        friends = len(Friend.objects.filter(from_user=request.user,to_user=User.objects.get(username=username)))
        
        if requested > 0:
            return "Requested"
        if friends > 0:
            return "Friends"
        else:
            return "None"

    related = check_relation(username)
    return render(request,"networking/profile.html",context={"user_info":u,"related":related})


@login_required
def friend(request,operation,usernameone,usernametwo):

    u1 = User.objects.get(username=usernameone)
    u2 = User.objects.get(username=usernametwo)
    
    if operation=="add":
        #Friends.add_friend(u1,u2)
        #Friends.add_friend(u2,u1)
        Friend.objects.add_friend(u1,u2)

    if operation=="remove":
        #Friends.remove_friend(u1,u2)
        #Friends.remove_friend(u2,u1)
        Friend.objects.remove_friend(u1,u2)

    if operation=="pull_request":
        FriendshipRequest.objects.get(from_user=u1,to_user=u2).delete()
    
    return HttpResponseRedirect(reverse('networking:profile',args=(usernametwo,))) 

@login_required
def project_view(request,project_id):
    info = ProjectCreation.objects.get(id=project_id)
    applied = len(ProjectInductionRequest.objects.filter(user=request.user,project__id=project_id))>0
    a_part = len(ProjectMembers.objects.filter(member=request.user,project__id=project_id))>0

    return render(request,"networking/project_details.html",context={"project_info":info,
                                                                     "applied":str(applied),
                                                                     "a_part":str(a_part)})

