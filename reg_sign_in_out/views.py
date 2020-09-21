from django.shortcuts import render
from reg_sign_in_out.models import *
from . import forms 

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
import razorpay 

def index(request):
    return render(request,"index.html")

@login_required
def special(request):
    return HttpResponse("In!")

@login_required
def user_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))  

@csrf_protect
def registration(request):

    registered = False

    
    if request.method == "POST":
        form = forms.UserForm(request.POST)
        profileform = forms.RegistrationForm(request.POST,request.FILES)

        if form.is_valid() and profileform.is_valid():
            
            user = form.save()
            user.set_password(user.password)
            user.save()

            profile = profileform.save(commit=False)
            profile.user = user
            
            profile.save()

            registered = True

            return HttpResponseRedirect(reverse('reg_sign_in_out:payment'))  
        else:

            print(form.errors,profileform.errors)
            
            return render(request,"reg_sign_in_out/registration.html",{"tried":"True",
                                                    "registered":registered,
                                                   "profile_form":profileform,
                                                   "user_form":form,
                                                   })
            

    else:
        user = forms.UserForm()
        profileform = forms.RegistrationForm()

    return render(request,"reg_sign_in_out/registration.html",{"registered":registered,
                                                   "profile_form":profileform,
                                                   "user_form":user,
                                                   })


@csrf_protect
def user_login(request):

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username,password=password)
        if user:
            if user.is_active:
                login(request,user)
                return HttpResponseRedirect(reverse('posts:home'))

        else:

            return render(request,"reg_sign_in_out/login.html",{'tried':'True'})

    else:
        return render(request,"reg_sign_in_out/login.html")

@login_required
def payment(request):
    obj = Registration.objects.get(user__username=request.user.username)
    if obj.paid==False:
        client = razorpay.Client(auth = ('rzp_test_iCqL53D2oVdlIL', 'A5bcZDlcdxB6qz5K6O4i5eD1'))   
        payment = client.order.create({'amount':10000000, 'currency':'INR', 'payment_capture':'1'})

        if request.method=="POST":
            
            obj.paid = True
            obj.order_id = request.POST["razorpay_order_id"]
            obj.save()
            return HttpResponseRedirect(reverse('profilepage:profilepage'))

        return render(request,"reg_sign_in_out/payment.html",{'payment':payment})
    else:
        return render(request,"reg_sign_in_out/paid.html")