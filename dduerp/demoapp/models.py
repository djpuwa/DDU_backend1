
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
class User(models.Model):
    email=models.EmailField()
    password=models.CharField(max_length=40)
    firstName=models.CharField(max_length=30,default='John')
    lastName=models.CharField(max_length=30,default='Wick')
    
    # class Meta:
    #     ordering = ['-date_created']

    def __self__(self):
        return self.email

class ExtendUser(AbstractUser):
    id=models.AutoField(primary_key=True)
    email = models.EmailField()


    USERNAME_FIELD = 'username'
    EMAIL_FIELD='email'
    
    def __self__(self):
        return self.id

# class TempAdd(models.Model):
#     email=models.EmailField()
#     password=models.CharField(max_length=40)
#     firstName=models.CharField(max_length=30,default='John')
#     lastName=models.CharField(max_length=30,default='Wick')
    
#     # class Meta:
#     #     ordering = ['-date_created']

#     def __self__(self):
#         return self.email