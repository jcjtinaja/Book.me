from django.contrib import admin
from .models import Appointment, ChangeLog

# Register your models here.

admin.site.register(Appointment)
admin.site.register(ChangeLog)