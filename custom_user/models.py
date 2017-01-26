from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import AbstractUser

class customUser(AbstractUser):
    pic = models.ImageField(null = True, blank = True, default = None, upload_to='user_pic')
    points = models.IntegerField(default=0)
