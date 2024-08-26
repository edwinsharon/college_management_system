from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name="index"),
    path('adminsignin',views.adminsignin,name="adminsignin"),
    path('admindash',views.admindash,name="admindash"),
    path('admindashstudents',views.admindashstudents,name="admindashstudents"),
    
]