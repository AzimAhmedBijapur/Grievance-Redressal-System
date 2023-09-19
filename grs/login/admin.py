from django.contrib import admin
from .models import CustomUser, Complaint

admin.site.register(CustomUser)
admin.site.register(Complaint)
