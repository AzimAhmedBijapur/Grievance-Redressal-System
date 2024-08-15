from django.contrib import admin
from .models import Complaint

class ComplaintsAdmin(admin.ModelAdmin):
    list_display = ('subject','user' ,'date', 'category','status',)
    fields = ('user', 'category', 'subject', 'description', 'date', 'documents', 'report', 'escalatetoHo', 'severity', 'due_date', 'status')
    readonly_fields = ('user', 'category', 'subject', 'description', 'date', 'documents', 'report', 'escalatetoHo', 'severity', 'due_date')


admin.site.register(Complaint, ComplaintsAdmin)