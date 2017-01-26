from custom_user.models import customUser
from django import http
from django.db import models

def user_processor(request):
    users = customUser.objects.all().order_by('-points')
    return {'users': users}
