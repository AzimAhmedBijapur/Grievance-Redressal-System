from django.urls import path
from . import views

urlpatterns = [
    path("ho",views.ho,name="ho"),
    path("ho/view/complaints",views.viewComplaints,name="ho/view/complaints"),
    path("ho/view/complaints/<int:cid>",views.viewDetailComplaints,name="ho/view/complaint"),
]