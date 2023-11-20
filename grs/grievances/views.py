from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import Http404,HttpResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from grievances.models import Complaint
from django.core.mail import send_mail
from django.db.models import Q
import os
from pathlib import Path
from grs.decorators import role_required, admin_required
from login.models import CustomUser


@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_required
def download_complaint_documents(request, filename):
    file_directory = "/home/AzimAhmedBijapur/Grievance-Redressal-System/grs/complaints/documents/"
    file_path = os.path.join(file_directory, filename)

    print("File Path:", file_path)  # Add this line for debugging

    if os.path.exists(file_path):
        # If the file exists, serve it using FileResponse
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else:
        print("File not found")  # Add this line for debugging
        raise Http404("File not found")


# Download reports
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_required
def download_complaint_reports(request, filename):
    file_directory = "/home/AzimAhmedBijapur/Grievance-Redressal-System/grs/complaints/reports/"
    file_path = os.path.join(file_directory, filename)
    print(file_path)
    if os.path.exists(file_path):
        # If the file exists, serve it for download
        with open(file_path, 'rb') as file:
            response = HttpResponse(
                file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        # If the file does not exist, return an error response
        return HttpResponse("File not found", status=404)


