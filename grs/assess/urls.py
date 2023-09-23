from django.urls import path, include
from .views import assessDashboard, viewComplaints, detailComplaints

urlpatterns = [
    path('assess', assessDashboard, name='assess'),
    path('assess/view/complaints', viewComplaints, name='assess/view/complaints'),
    path('assess/view/complaint/<int:cid>', detailComplaints, name='assess/view/complaint'),

]
