from operator import mod
from unicodedata import name
from django.db import models
from accounts.models import ExtendUser

# Create your models here.


class Faculty(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    shortName=models.CharField(max_length=10)
    dean = models.ForeignKey(ExtendUser, on_delete=models.SET_NULL,null=True)

    def __self__(self):
        return self.name

class Department(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=30)
    shortName=models.CharField(max_length=10)
    faculty=models.ForeignKey(Faculty,on_delete=models.CASCADE)
    head=models.ForeignKey(ExtendUser, on_delete=models.SET_NULL,null=True)

    def __self__(self):
        return self.name

class Program(models.Model):
    id=models.AutoField(primary_key=True)
    name=models.CharField(max_length=50)
    type=models.CharField(max_length=30)
    degree=models.CharField(max_length=15)
    faculty=models.ForeignKey(Faculty, on_delete=models.CASCADE)
    department=models.ForeignKey(Department,on_delete=models.CASCADE)
    duration=models.FloatField()
    sessionalType=models.CharField(max_length=20)
    maxSessions=models.IntegerField()

    def __self__(self):
        return self.name

class ExamSchemeHead(models.Model):
    id=models.AutoField(primary_key=True)
    external=models.IntegerField()
    sessional=models.IntegerField()
    practical=models.IntegerField()
    teamwork=models.IntegerField()
    maxMarks=models.IntegerField()
    minMarks=models.IntegerField()

    def __self__(self):
        return self.id    

class TeachingSchemeHead(models.Model):
    id=models.AutoField(primary_key=True)
    lectures=models.IntegerField()
    tutorials=models.IntegerField()
    labs=models.IntegerField()

    def __self__(self):
        return self.id

class Subject(models.Model):
    code=models.CharField(max_length=15,primary_key=True)
    name=models.CharField(max_length=30)
    shortName=models.CharField(max_length=10)
    teachingScheme=models.ForeignKey(TeachingSchemeHead,on_delete=models.SET_NULL,null=True)
    examScheme=models.ForeignKey(ExamSchemeHead,on_delete=models.SET_NULL,null=True)

    def __self__(self):
        return self.name