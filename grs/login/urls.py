from django.urls import path, include
from . import views

urlpatterns = [
    path("register",views.register,name="register"),
    path("add/management/staff/",views.registerManagementStaff,name="add/management/staff/"),
    path("login",views.loginPage,name="login"),
    path("logout",views.logoutUser,name="logout"),
    path("",views.index,name="index"),

    path("faculty",views.faculty,name="faculty"),
    path("add/complaint",views.addComplaint,name="add/complaint"),
    path("view/MyComplaints",views.viewMyComplaints,name="view/MyComplaints"),
   path('view/reports/<str:filename>', views.download_complaint_report, name='download_complaint_report'),
   path('complaints/documents/<str:filename>', views.download_complaint_document, name='download_complaint_document'),

]
