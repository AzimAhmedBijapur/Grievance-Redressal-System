from pathlib import Path
from django.http import HttpResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
from grs.decorators import role_required
import os
import environ

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Download supporting documents
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@role_required(allowed_roles=['Assessment Committee','Review Committee', 'HO', 'Faculty'])
def download_complaint_doc(request, filename):
    file_directory = env("DOCUMENTS_FILE_PATH")
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


# Download reports
@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@role_required(allowed_roles=['Assessment Committee','Review Committee', 'HO', 'Faculty'])
def download_complaint_reports(request, filename):
    file_directory = env("REPORTS_FILE_PATH")
    file_path = os.path.join(file_directory, filename)
    print(file_path)
    if os.path.exists(file_path):
        # If the file exists, serve it for download
        print('exists')
        with open(file_path, 'rb') as file:
            response = HttpResponse(
                file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="{filename}"'
            return response
    else:
        # If the file does not exist, return an error response
        return HttpResponse("File not found", status=404)