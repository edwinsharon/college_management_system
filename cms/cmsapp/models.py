from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.
class Verify(models.Model):
    otp = models.IntegerField()
    otp1 = models.IntegerField()

class College(models.Model):
    department = models.CharField(max_length=50)
    semester = models.CharField(max_length=100)

class Students(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    department = models.ForeignKey(College, on_delete=models.CASCADE)
    is_first_login = models.BooleanField(default=True) 
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_staff')  # Updated related_name

class Exam(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    semester = models.ForeignKey(College, on_delete=models.CASCADE)
    mark = models.IntegerField()
    
    def __str__(self):
        return self.title

class Faculties(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age = models.IntegerField()
    department = models.ForeignKey(College, on_delete=models.CASCADE)
    is_first_login = models.BooleanField(default=True) 
    staff = models.ForeignKey(User, on_delete=models.CASCADE, related_name='faculty_staff')  # Updated related_name
