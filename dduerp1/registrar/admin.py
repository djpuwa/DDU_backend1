from django.contrib import admin
from .models import *
from django.apps import apps
# Register your models here.


admin.site.register(Faculty)
admin.site.register(Department)
admin.site.register(Program)
admin.site.register(ExamSchemeHead)
admin.site.register(TeachingSchemeHead)
admin.site.register(Subject)
admin.site.register(ExamScheme)
admin.site.register(TeachingScheme)
admin.site.register(SubjectExam)
admin.site.register(SubjectTeaching)