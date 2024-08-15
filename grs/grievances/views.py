from pathlib import Path
from django.http import FileResponse, Http404,HttpResponse
from django.views.decorators.cache import cache_control
from django.contrib.auth.decorators import login_required
import os
import environ
from grs.decorators import admin_required

env = environ.Env()
BASE_DIR = Path(__file__).resolve().parent.parent
environ.Env.read_env(os.path.join(BASE_DIR, '.env'))

# Download documents and reports only for admin

# Download supporting documents

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_required
def download_complaint_documents(request, filename):
    file_directory = env("DOCUMENTS_FILE_PATH")
    file_path = os.path.join(file_directory, filename)

    if os.path.exists(file_path):
        # If the file exists, serve it using FileResponse
        response = FileResponse(open(file_path, 'rb'), content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="{filename}"'
        return response
    else: 
        raise Http404("File not found")


# Download reports

@login_required(login_url='login')
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
@admin_required
def download_complaint_reports(request, filename):
    file_directory = env("REPORTS_FILE_PATH")
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


