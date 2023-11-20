
from django.urls import path
from . import views

urlpatterns = [
        # for admin
    path('complaints/documents/<str:filename>', views.download_complaint_documents, name='download_complaint_documents'),
    path('complaints/reports/<str:filename>', views.download_complaint_reports, name='download_complaint_reports'),
]