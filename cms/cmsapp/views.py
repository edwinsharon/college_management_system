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
# Create your views here.
def index(request):
    return render(request,'index.html')
def stafflogin(request):
    if 'username' in request.session:
        if is_staff:
            return redirect('staffdash')
        else:
            return redirect('index')
    if request.POST:
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            request.session['username']=username
            return redirect("sellerindex")
    return render(request,"sellerlogin.html") 

def adminsignin(request):
     if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_super:
                login(request, user)
                request.session['username'] = username
                return redirect('admindash') 
            else :
                return redirect("index")
        return render(request,"adminsignin.html")        

def admindash(request):
    return render(request,"admindash.html")   
def admindashstudents(request):
    return render(request,"admindashstudents.html")
def addstaff(request):
    if request.POST:
        email=request.POST.get('email')
        username=request.POST.get('username')
        
        if not username or not email or not password or not confirmpassword:
            messages.error(request,'all fields are required.')

        elif confirmpassword != password:
            messages.error(request,"password doesnot match")
           
        elif User.objects.filter(email=email).exists():
            messages.error(request,"email already exist")
           
        elif User.objects.filter(username=username).exists():
            messages.error(request,"username already exist")

        else:
           
            user = User.objects.create_user(username=username, email=email, password=password)    
            user.is_staff=True
            user.save()
    return render(request,"addstaff.html")
