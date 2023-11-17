from django.db import models
import uuid
from login.models import CustomUser
from django.db import models
from django.db.models.signals import pre_delete
from django.dispatch import receiver
import os


def document_upload_to(instance, filename):
    unique_filename = str(uuid.uuid4())
    file_extension = filename.split('.')[-1]
    final_filename = f"{unique_filename}.{file_extension}"
    return f"documents/{final_filename}"

def report_upload_to(instance, filename):
    unique_filename = str(uuid.uuid4())
    file_extension = filename.split('.')[-1]
    final_filename = f"{unique_filename}.{file_extension}"
    return f"reports/{final_filename}"

class Complaint(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    category = models.CharField(max_length=100)
    subject = models.CharField(max_length=300)
    description = models.TextField()
    date = models.DateField(null=True, blank=True)
    documents = models.FileField(upload_to=document_upload_to, blank=True, null=True)
    status = models.CharField(max_length=100,default="Unsolved",choices=[('Solved','Solved'),('Unsolved','Unsolved'),('In-Progress','In-Progress'),('Rejected','Rejected')])
    # Assessment committee
    report = models.FileField(upload_to=report_upload_to,null=True,blank=True,)
    # review committee
    escalatetoHo = models.CharField(max_length=100,default="No",choices=[('Yes','Yes'),('No','No')])
    severity = models.CharField(max_length=100,blank=True,null=True,default='4')
    due_date = models.DateField(null=True,blank=True)


    def __str__(self):
        return self.subject


@receiver(pre_delete, sender=Complaint)
def delete_complaint_documents(sender, instance, **kwargs):
    if instance.documents:
        file_path = instance.documents.path
        if os.path.exists(file_path):
            os.remove(file_path)