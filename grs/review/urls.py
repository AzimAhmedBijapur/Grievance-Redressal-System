from django.urls import path
from . import views

urlpatterns = [
    path("review",views.review,name="review"),
    path("review/view/complaints",views.viewComplaints,name="review/view/complaints"),
    path("review/view/complaints/<int:cid>",views.viewDetailComplaints,name="review/view/complaint"),
]
