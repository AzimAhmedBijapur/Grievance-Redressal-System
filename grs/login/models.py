from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
import uuid

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=100, blank=True)
    role = models.CharField(max_length=50, choices=[('Review Committee', 'Review Committee'), ('Assessment Committee', 'Assessment Committee'), ('HO', 'HO'),('Faculty','Faculty')])
    gender = models.CharField(max_length=1, choices=[('M', 'Male'), ('F', 'Female'), ('O', 'Other')], blank=True)
    contact_no = models.CharField(max_length=15, blank=True)
    telephone_no = models.CharField(max_length=15, blank=True)
    current_address = models.CharField(max_length=150, blank=True)
    permanent_address = models.CharField(max_length=150, blank=True)
    educational_qualification = models.CharField(max_length=100, blank=True)
    department = models.CharField(max_length=50, blank=True)
    designation = models.CharField(max_length=50, blank=True)
    permanent_employee = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')], blank=True)
    date_of_probation = models.DateField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    payscale = models.CharField(max_length=20, blank=True)
    

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'

def document_upload_to(instance, filename):
    unique_filename = str(uuid.uuid4())
    file_extension = filename.split('.')[-1]
    final_filename = f"{unique_filename}.{file_extension}"
    return f"complaints/documents/{final_filename}"

def report_upload_to(instance, filename):
    unique_filename = str(uuid.uuid4())
    file_extension = filename.split('.')[-1]
    final_filename = f"{unique_filename}.{file_extension}"
    return f"complaints/reports/{final_filename}"

class Complaint(models.Model):
    user = models.ForeignKey(CustomUser,default=None, on_delete=models.CASCADE)
    category = models.CharField(max_length=100)
    subject = models.CharField(max_length=300)
    description = models.TextField()
    documents = models.FileField(upload_to=document_upload_to, blank=True, null=True)
    # These fields are to be set by mgmt staff and admin only
    status = models.CharField(max_length=100,default="Unsolved",choices=[('Solved','Solved'),('Unsolved','Unsolved'),('In-Progress','In-Progress')])
    severity = models.CharField(max_length=100,blank=True,null=True)
    due_date = models.DateField(null=True,blank=True)
    report = models.FileField(upload_to=report_upload_to,null=True,blank=True)


    def __str__(self):
        return self.subject