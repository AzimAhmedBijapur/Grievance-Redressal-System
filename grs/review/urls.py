from django.urls import path
from . import views
from grs.uploadAndDownload import download_complaint_doc, download_complaint_reports

urlpatterns = [
    path("review",views.review,name="review"),
    path("review/view/complaints",views.viewComplaints,name="review/view/complaints"),
    path("review/view/complaints/<int:cid>",views.viewDetailComplaints,name="review/view/complaint"),
    path('review/view/complaints/documents/<str:filename>', download_complaint_doc, name='download_complaint_doc'),
    path('review/view/complaints/reports/<str:filename>', download_complaint_reports, name='download_complaint_reports'),
]
