from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from posts.models import *
from friendship.models import FriendshipRequest,Block,Follow,Friend
from django.http import HttpResponseRedirect
from django.urls import reverse
from project_management.models import *
from . import forms
from reg_sign_in_out.models import Registration
from django.contrib.auth.models import User

@login_required
def profilepage(request):

    posts_obj = Posts.objects.filter(user=request.user)
    comment_obj = Comment.objects.filter(userid=request.user)
    friend_reqs = Friend.objects.requests(user=request.user)
    friend_list = Friend.objects.friends(request.user)
    project_req_list = ProjectInductionRequest.objects.filter(project__team_lead=request.user)
    paid_bool = Registration.objects.get(user=request.user).paid
    return render(request,"profilepage/profilepage.html",{"user":request.user,
                                                          "posts_obj":posts_obj,
                                                          "comment_obj":comment_obj,
                                                          "req_list":friend_reqs,
                                                          "friend_list":friend_list,
                                                          "project_req_list":project_req_list,
                                                          "paid_bool":paid_bool})
@login_required
def friendship_operation(request,operation,current_user,other_user):

    u1 = User.objects.get(username=current_user)
    u2 = User.objects.get(username=other_user)

    friend_request = FriendshipRequest.objects.get(to_user=u1,from_user=u2)

    if operation == "Reject":
        print(operation,"\n"*3)
        friend_request.delete()

    if operation == "Accept":
        friend_request.accept()

    if operation == "Remove":
        Friend.objects.remove_friend(u1, u2)

    return HttpResponseRedirect(reverse('profilepage:profilepage')) 

def projectmember(request,operation,username,project_id):

    u = User.objects.get(username=username)

    if operation=="Accept":
        ProjectMembers.func.add_member(request.user,u,project_id)

    if operation=="Reject":
        ProjectMembers.func.reject_member(u,project_id)

    if operation=="Remove":
        ProjectMembers.func.remove_member(u,project_id)

    return HttpResponseRedirect(reverse('profilepage:profilepage')) 


def changeprofileinfo(request):
 
    if request.method == "POST":
        form = forms.UserChangeForm(request.POST)
        profileform = forms.RegistrationChangeForm(request.POST,request.FILES)
        print(request.POST)
        if form.is_valid() and profileform.is_valid():
            
            # user = form.save(commit=False)
            # user = request.user
            # user.save()
            cuser = User.objects.get(username=request.user.username)

            if len(request.POST['first_name'])!=0:
                cuser.first_name = request.POST['first_name']
            if len(request.POST['last_name'])!=0:
                cuser.last_name = request.POST['last_name']
            if len(request.POST['email'])!=0:
                cuser.email = request.POST['email']
            cuser.save()

            Registration.objects.get(user=request.user).delete()
            profile = profileform.save(commit=False)
            profile.user = request.user
            
            profile.save()

            return HttpResponseRedirect(reverse('profilepage:profilepage'))

        else:

            print(form.errors,profileform.errors)
            
            return render(request,"profilepage/change.html",{"tried":"True",
                                                   "profile_form":profileform,
                                                   "user_form":form,
                                                   })
            

    else:
        form = forms.UserChangeForm()
        profileform = forms.RegistrationChangeForm()

    return render(request,"profilepage/change.html",{
                                                   "profile_form":profileform,
                                                   "user_form":form,
                                                   })