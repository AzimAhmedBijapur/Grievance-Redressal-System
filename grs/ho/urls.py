from django.urls import path
from . import views
from grs.uploadAndDownload import download_complaint_doc, download_complaint_reports

urlpatterns = [
    path("ho",views.ho,name="ho"),
    path("ho/view/complaints",views.viewComplaints,name="ho/view/complaints"),
    path("ho/view/complaints/<int:cid>",views.viewDetailComplaints,name="ho/view/complaint"),
    path('ho/view/complaints/documents/<str:filename>', download_complaint_doc, name='download_complaint_doc'),
    path('ho/view/complaints/reports/<str:filename>', download_complaint_reports, name='download_complaint_reports'),
]