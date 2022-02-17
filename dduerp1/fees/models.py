from django.db import models

# Create your models here.

class FeeStructureHead(models.Model):
    id=models.AutoField(primary_key=True)
    name =models.CharField(max_length=20)
    type=models.CharField(max_length=20)
    description=models.CharField(max_length=150)
    time_stamp=models.DateTimeField()

    def __self__(self):
        return self.name

class FeeStructureCategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=150)
    time_stamp=models.DateTimeField()

    def __self__(self):
        return self.name