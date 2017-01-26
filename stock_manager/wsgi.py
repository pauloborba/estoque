"""
WSGI config for stock_manager project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application
<<<<<<< HEAD
=======
from whitenoise.django import DjangoWhiteNoise
>>>>>>> First Commit

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stock_manager.settings")

application = get_wsgi_application()
<<<<<<< HEAD
=======
application = DjangoWhiteNoise(application)
>>>>>>> First Commit
