from django.contrib import admin
from .models import Faculty, Department, Program, ExamSchemeHead
from django.apps import apps
# Register your models here.


admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Program)
admin.site.register(ExamSchemeHead)