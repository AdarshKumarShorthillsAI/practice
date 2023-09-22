from django.contrib import admin
from .models import Message,CustomUser
# Register your models here.
admin.site.register(Message)
admin.site.register(CustomUser)
