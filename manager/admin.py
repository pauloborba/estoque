from django.contrib import admin
from .models import Item
from custom_user.models import customUser

admin.site.register(Item)
admin.site.register(customUser)
# Register your models here.
