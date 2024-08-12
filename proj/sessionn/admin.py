from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Session, GeeksModel


admin.site.register(Session)
admin.site.register(GeeksModel)