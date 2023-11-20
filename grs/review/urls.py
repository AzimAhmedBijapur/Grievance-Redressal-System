from django.urls import path
from . import views

urlpatterns = [
    path("review",views.review,name="review"),
    path("review/view/complaints",views.viewComplaints,name="review/view/complaints"),
    path("review/view/complaints/<int:cid>",views.viewDetailComplaints,name="review/view/complaint"),
    path('review/view/complaints/documents/<str:filename>', views.download_complaint_doc, name='download_complaint_doc'),
    path('review/view/complaints/reports/<str:filename>', views.download_complaint_reports, name='download_complaint_reports'),
]
