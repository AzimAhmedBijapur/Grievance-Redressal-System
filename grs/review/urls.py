from django.urls import path, include
from .views import reviewDashboard, viewComplaints, detailComplaints

urlpatterns = [
    path('review', reviewDashboard, name='review'),
    path('review/view/complaints', viewComplaints, name='review/view/complaints'),
    path('review/view/complaint/<int:cid>', detailComplaints, name='review/view/complaint'),
]
