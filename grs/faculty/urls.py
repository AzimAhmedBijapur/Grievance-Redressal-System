from django.urls import path
from . import views

urlpatterns = [
    path("faculty",views.faculty,name="faculty"),
    path("add/complaint",views.addComplaint,name="add/complaint"),
    path("view/MyComplaints",views.viewMyComplaints,name="view/MyComplaints"),
    path("view/MySolvedComplaints",views.viewMySolvedComplaints,name="view/MySolvedComplaints"),
    path('view/reports/<str:filename>', views.download_complaint_report, name='download_complaint_report'),

]