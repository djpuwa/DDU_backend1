from django.contrib import admin
from .models import User, ExtendUser

# Register your models here.
admin.site.register(User)
admin.site.register(ExtendUser)