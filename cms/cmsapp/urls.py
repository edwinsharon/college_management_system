from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',views.index,name="index"),
    path('adminsignin',views.adminsignin,name="adminsignin"),
    path('admindash',views.admindash,name="admindash"),
    path('admindashstudents',views.admindashstudents,name="admindashstudents"),
    path('addstaff',views.addstaff,name="addstaff"),
    path('loginuser',views.loginuser,name="loginuser"),
    # path("createadmin",views.createadmin,name="createadmin",),
    path('staff',views.staff,name="staff"),
    path('logoutuser',views.logoutuser,name='logoutuser'),
    path('removeuser/<int:pk>',views.delete_a,name='removeuser'),
    path('forgotpassword',views.forgotpassword,name="forgotpassword"),
    path('getotp',views.getotp,name="getotp"),
    path('changepassword',views.changepassword,name="changepassword"),
    path('addstudents',views.addstudents,name='addstudents'),
    path('add_department',views.add_department,name='add_department'),
    path('delete_department/<int:pk>',views.delete_department,name='delete_department'),
    path('add_exam',views.add_exam,name='add_exam'),
    path('add_semester',views.add_semester,name='add_semester'),

]
if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)