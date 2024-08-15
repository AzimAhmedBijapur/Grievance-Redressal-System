from django.urls import path
from . import views
from grs.uploadAndDownload import download_complaint_doc, download_complaint_reports

urlpatterns = [
    path("assessment",views.assessment,name="assessment"),
    path("assessment/view/complaints",views.viewComplaints,name="assessment/view/complaints"),
    path("assessment/view/complaints/<int:cid>",views.viewDetailComplaints,name="assessment/view/complaint"),
    path('assessment/view/complaints/documents/<str:filename>',download_complaint_doc , name='download_complaint_doc'),
    path('assessment/view/complaints/reports/<str:filename>', download_complaint_reports, name='download_complaint_reports'),

]