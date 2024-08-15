from django.contrib import admin
from .models import CustomUser
from allauth.socialaccount.models import SocialToken, SocialAccount, SocialApp, EmailAddress
from django.contrib.auth.models import Group

class CustomUserAdmin(admin.ModelAdmin):
    # Display full_name in the list view along with any other fields you want
    list_display = ('full_name', 'email', 'role', 'gender', 'is_superuser')

    # Make all fields readonly but visible in the admin form view
    readonly_fields = (
        'username', 'password', 'full_name','email', 'role', 'gender',
        'contact_no', 'telephone_no', 'current_address', 
        'permanent_address', 'educational_qualification', 
        'department', 'designation', 'permanent_employee', 
        'date_of_probation', 'salary', 'payscale', 'otp'
    )

    # This defines the order in which fields appear in the form view
    fieldsets = (
        (None, {
            'fields': ('username', 'password', 'full_name', 'email', 'role', 'gender', 'is_superuser')
        }),
        ('Contact Information', {
            'fields': ('contact_no', 'telephone_no', 'current_address', 'permanent_address')
        }),
        ('Job Information', {
            'fields': ('department', 'designation', 'permanent_employee', 'date_of_probation', 'salary', 'payscale')
        }),
    )

admin.site.register(CustomUser, CustomUserAdmin)

# admin.site.unregister(Group)