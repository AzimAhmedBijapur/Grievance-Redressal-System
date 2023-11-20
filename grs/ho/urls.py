from django.urls import path
from . import views

urlpatterns = [
    path("ho",views.ho,name="ho"),
    path("ho/view/complaints",views.viewComplaints,name="ho/view/complaints"),
    path("ho/view/complaints/<int:cid>",views.viewDetailComplaints,name="ho/view/complaint"),
    path('ho/view/complaints/documents/<str:filename>', views.download_complaint_doc, name='download_complaint_doc'),
    path('ho/view/complaints/reports/<str:filename>', views.download_complaint_reports, name='download_complaint_reports'),
]