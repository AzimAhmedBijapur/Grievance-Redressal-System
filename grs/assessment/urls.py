from django.urls import path
from . import views

urlpatterns = [
    path("assessment",views.assessment,name="assessment"),
    path("assessment/view/complaints",views.viewComplaints,name="assessment/view/complaints"),
    path("assessment/view/complaints/<int:cid>",views.viewDetailComplaints,name="assessment/view/complaint"),
]