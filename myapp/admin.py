from django.contrib import admin
from myapp.models import *
# Register your models here.
admin.site.register(User)
admin.site.register(emailverification)
admin.site.register(Ticket)
admin.site.register(Contact)

# If you have a custom User model, ensure it inherits from AbstractUser and is set in settings.py:
# AUTH_USER_MODEL = 'myapp.User'

# If you have a custom UserAdmin, register like this:
# from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
# from .models import User
# admin.site.register(User, BaseUserAdmin)

# If you have not created a superuser, run:
# python manage.py createsuperuser
