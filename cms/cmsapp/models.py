from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.
class Verify(models.Model):
    otp = models.IntegerField()
    otp1 = models.IntegerField()


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    age=models.IntegerField()
    department=models.CharField(max_length=50)


class Semester(models.Model):
    name = models.CharField(max_length=50)
    start_date = models.DateField()
    end_date = models.DateField()
    staff= models.ForeignKey(User, on_delete=models.CASCADE, related_name='products_sold')
    def __str__(self):
        return self.name


class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    is_submitted = models.BooleanField(default=False) 
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    def __str__(self):
        return self.title

class Exam(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    semester = models.ForeignKey(Semester, on_delete=models.CASCADE)
    mark=models.IntegerField()
    def __str__(self):
        return self.title

class CustomUser(AbstractUser):
    is_first_login = models.BooleanField(default=True)   

    
