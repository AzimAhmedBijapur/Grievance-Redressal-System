from django.urls import path
from . import views
from grs.uploadAndDownload import download_complaint_doc, download_complaint_reports

urlpatterns = [
    path("faculty",views.faculty,name="faculty"),
    path("add/complaint",views.addComplaint,name="add/complaint"),
    path("view/MyComplaints",views.viewMyComplaints,name="view/MyComplaints"),
    path("view/MySolvedComplaints",views.viewMySolvedComplaints,name="view/MySolvedComplaints"),
    path('view/reports/<str:filename>', download_complaint_reports, name='download_complaint_report'),
    path('view/documents/<str:filename>', download_complaint_doc, name='download_complaint_doc'),

]