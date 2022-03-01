
from django.db import models
from django.contrib.auth.models import AbstractUser
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.

class UserRole(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=150)

    def __self__(self):
        return self.name

class ExtendUser(AbstractUser):
    id=models.AutoField(primary_key=True)
    email = models.EmailField()
    
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL,null=True)

    USERNAME_FIELD = 'username'
    EMAIL_FIELD='email'
    
class Temp(models.Model):
    title=models.CharField(max_length=100)

    def __self__(self):
        return self.title
    

class UserProfile(models.Model):
    # id = models.AutoField()
    primaryContact = PhoneNumberField(null=False, blank=False, unique=True)
    photo = models.ImageField(upload_to='images')
    secondaryContact = PhoneNumberField()
    currentAdd = models.CharField(max_length=40)
    currentCity = models.CharField(max_length=20)
    currentState = models.CharField(max_length=20)
    permAdd = models.CharField(max_length=40)
    permCity = models.CharField(max_length=20)
    permState = models.CharField(max_length=20)
    altEmail = models.EmailField()
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    bloodGroup = models.CharField(max_length=10)
    user = models.ForeignKey(ExtendUser,on_delete=models.CASCADE)

    def __self__(self):
        return self.user.email



