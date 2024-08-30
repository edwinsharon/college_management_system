from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from verify_email.email_handler import send_verification_email
from django.conf import settings
from django.core.mail import send_mail
import random
from django.urls import reverse
from django.utils.crypto import get_random_string
# Create your views here.
def index(request):
    return render(request,'index.html')
def loginuser(request):
    if request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')
        print(username,password)
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            request.session['username']=username
            if user.is_staff:
                return redirect('staffdash')
            elif user.is_superuser:
                return redirect('admindash')
            else:
                return redirect('studentdash')
    return render(request,"adminsignin.html") 

def adminsignin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            request.session['username']=username
            if user.is_staff:
                return redirect('staffdash')
            elif user.is_superuser:
                return redirect('admindash')
            else:
                return redirect('studentdash')
    return render(request,"adminsignin.html")        

def admindash(request):
    staff_profiles = Profile.objects.filter(staff=True)
    return render(request,"admindash.html",{"staff_profiles":staff_profiles})   
def admindashstudents(request):
    staff_profiles = Profile.objects.all()
    return render(request,"admindashstudents.html",{"staff_profiles":staff_profiles})
def addstaff(request):
    if request.POST:
        email=request.POST.get('email')
        username=request.POST.get('username')
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        age=request.POST.get('age')
        department=request.POST.get('department')
        staff=request.user
        if not username or not email:
            messages.error(request,'all fields are required.')
      
           
        elif User.objects.filter(email=email).exists():
            messages.error(request,"email already exist")
           
        elif User.objects.filter(username=username).exists():
            messages.error(request,"username already exist")

        else:
            password = get_random_string(length=12)
            message = f'Your Password for Teslas System is: {password}. your username is :{username}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail('Email Verification', message, email_from, recipient_list)
            user = User.objects.create_user(username=username, email=email, password=password)    
            profile = Profile(first_name=first_name, last_name=last_name, age=age, department=department,user=user,staff=staff)   
            user.is_staff=True
            user.save()
            profile.save()
            messages.success(request, "Staff member added successfully.")
            return redirect("admindash")
    return render(request,"addstaff.html")


def handle_first_login(sender, request, user, **kwargs):
    if hasattr(user, 'is_first_login') and user.is_first_login:
        user.is_first_login = False
        user.save()
        return redirect(reverse('first_login_welcome'))
    


def addstudents(request):
    if request.POST:
        email=request.POST.get('email')
        username=request.POST.get('username')
        first_name=request.POST.get('firstname')
        last_name=request.POST.get('lastname')
        age=request.POST.get('age')
        department=request.POST.get('department')
        staff=request.user
        if not username or not email:
            messages.error(request,'all fields are required.')   
        elif User.objects.filter(email=email).exists():
            messages.error(request,"email already exist")   
        elif User.objects.filter(username=username).exists():
            messages.error(request,"username already exist")
        else:
            password = get_random_string(length=12)
            message = f'Your Password for Teslas System is: {password}. your username is :{username}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail('Email Verification', message, email_from, recipient_list)
            user = User.objects.create_user(username=username, email=email, password=password)    
            profile = Profile(first_name=first_name, last_name=last_name, age=age, department=department,user=user,staff=staff)   
            user.save()
            profile.save()
            messages.success(request, "Staff member added successfully.")
            return redirect("admindash")
    return render(request,"addstaff.html")

def deletestaff(request,pk):
    prodobj=Profile.objects.get(pk=pk)
    prodobj.delete()
    return redirect("admindash")


def staff(request,pk):
    return render(request,"staff.html")

def logoutuser(request):
    logout(request)
    request.session.flush()
    return redirect('index')

# def createadmin(request):
#     username="mainadmin"
#     email="edwinmadapallil@gmail.com"
#     password="tesla@2002"
#     user = User.objects.create_user(username=username, email=email, password=password) 
#     user.is_superuser=True
#     user.save()
#     return HttpResponse("helloworld")   

# def staff(request,pk):
#     user = request.user
#     if user is not None:
#         students = Profile.objects.filter(staff=user)
#         return render(request,"staff.html",{"students":students})
#     else:
#         return redirect("loginuser")