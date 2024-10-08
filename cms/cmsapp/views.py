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
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            request.session['username']=username
            print("hai")
            if user.is_staff:
                # if user.is_first_login:
                #     logout(request)
                #     user.is_first_login = False
                #     user.save()
                #     return redirect('changepassword')

                return redirect('staff')
            elif user.is_superuser:
                return redirect('admindash')
            else:
                # if user.is_first_login:
                #     logout(request)
                #     user.is_first_login = False
                #     user.save()
                #     return redirect('changepassword')
                return HttpResponse ("studentdash")
    return render(request,"adminsignin.html") 

def adminsignin(request):
    user = request.user
    if 'username' in request.session:
        if user.is_staff:
                return redirect('staff')
        elif user.is_superuser:
                return redirect('admindash')
        else:
            return redirect('studentdash')


    elif request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request,user)
            request.session['username']=username
            if user.is_staff:
                if user.is_first_login:
                    logout(request)
                    user.is_first_login = False
                    user.save()
                    return redirect('changepassword')
                return redirect('staff')
            elif user.is_superuser:
                return redirect('admindash')
            else:
                if user.is_first_login:
                    logout(request)
                    user.is_first_login = False
                    user.save()
                    return redirect('changepassword')
                return redirect('studentdash')
    return render(request,"adminsignin.html")        

def admindash(request):
    staff_profiles = Faculties.objects.filter(staff=True)
    department=College.objects.all()
    return render(request,"admindash.html",{"staff_profiles":staff_profiles ,"department":department})   
def admindashstudents(request):
    staff_profiles = Students.objects.filter(staff=False)
    department=College.objects.all()
    return render(request,"admindashstudents.html",{"staff_profiles":staff_profiles, "department":department})
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
            department = College.objects.get(department=department)
            password = get_random_string(length=12)
            message = f'Your Password for Teslas System is: {password}. your username is :{username}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail('Email Verification', message, email_from, recipient_list)
            user = User.objects.create_user(username=username, email=email, password=password)    
            profile = Faculties(first_name=first_name, last_name=last_name, age=age, department=department,user=user,staff=staff)   
            user.is_staff=True
            user.save()
            profile.save()
            messages.success(request, "Staff member added successfully.")
            return redirect("admindash")
    department=College.objects.all()
    return render(request,"addstaff.html",{"department":department})


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
            department = College.objects.get(department=department)
            password = get_random_string(length=12)
            message = f'Your Password for Teslas System is: {password}. your username is :{username}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [email]
            send_mail('Email Verification', message, email_from, recipient_list)
            user = User.objects.create_user(username=username, email=email, password=password)    
            profile = Students(first_name=first_name, last_name=last_name, age=age, department=department,user=user,staff=staff)   
            user.save()
            profile.save()
            messages.success(request, "Staff member added successfully.")
            return redirect("staff")
    department=College.objects.all()
    return render(request,"addstudent.html",{"department":department})

def deletestaff(request,pk):
    prodobj=Faculties.objects.get(pk=pk)
    prodobj.delete()
    return redirect("admindash")


def staff(request):
    user = request.user
    profiles = Students.objects.filter(staff=user)
    return render(request,"staffdash.html",{"profiles":profiles})

def logoutuser(request):
    logout(request)
    request.session.flush()
    return redirect('index')

def delete_a(request,pk):
    prodobj=Students.objects.get(pk=pk)
    prodobj.delete()
    main=request.user
    if main.is_superuser:
        return redirect("admindash")
    else:
        return redirect("staff")
    

def forgotpassword(request):
    if request.POST:
        username=request.POST.get("username")
        main=User.objects.get(username=username)
        request.session['email']=main.email
        if main is not None:
            otp = ''.join(random.choices('123456789', k=6))
            request.session['otp'] = otp
            message = f'Your otp for Teslas System is: {otp}. your username is :{username}'
            email_from = settings.EMAIL_HOST_USER
            recipient_list = [main.email]
            send_mail('Email Verification', message, email_from, recipient_list)
            return redirect("getotp")
            

    return render(request,"forgotpassword.html")

def getotp(request):
    if request.method == 'POST':
        otp_from_form = request.POST.get('otp1')
        otp_from_session = request.session.get('otp')
        if otp_from_form == otp_from_session:
            del request.session['otp']  
            return redirect('changepassword')  
    return render(request,"getotp.html")

def changepassword(request):
    if request.method == 'POST':
        password=request.POST.get('password')
        confirmpassword=request.POST.get('confirmpassword')
        if password==confirmpassword:
            email=request.session.get('email')
            user = User.objects.get(email=email)
            user.set_password(password)
            user.save()
            request.session.flush()
            return redirect('adminsignin')
    return render(request,"changepassword.html")


def add_department(request):
    if request.method == 'POST':
        department=request.POST.get('department')
        dep=College(department=department)
        dep.save()
        return redirect("add_department")
    department=College.objects.all()
    return render(request,"adddepartment.html",{"department":department})

def delete_department(request,pk):
    prodobj=College.objects.get(pk=pk)
    prodobj.delete()
    return redirect("add_department")


def add_exam(request):
    if request.method == 'POST':
        title=request.POST.get("title")
        date=request.POST.get("date")
        semester=request.POST.get("semester")
        mark=request.POST.get("mark")
        dep=Exam(title=title,date=date,semester=semester,mark=mark)
        dep.save()
        return redirect("add_exam")
    return render(request,"addexam.html")


def add_semester(request):
    if request.method == 'POST':
        semester=request.POST.get('semester')
        dep=Semester(semester=semester)
        dep.save()
        return redirect("add_semester")
    semester=Semester.objects.all()
    return render(request,"addsemester.html",{"semester":semester})


# def createadmin(request):
#     username="teslaadmin"
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