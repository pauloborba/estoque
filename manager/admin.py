from django.contrib import admin
from .models import *
from custom_user.models import customUser

admin.site.register(Item)
admin.site.register(Category)
admin.site.register(customUser)
admin.site.register(Store)
admin.site.register(Price)
admin.site.register(Residence)
# Register your models here.
