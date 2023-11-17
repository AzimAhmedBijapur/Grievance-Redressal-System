from django.urls import path
from . import views

urlpatterns = [
    path("otp_verification", views.verify, name="otp_verification"),
    path("otp_input", views.otp_input, name="otp_input"),
    path("register", views.register, name="register"),
    path("add/management/staff/", views.registerManagementStaff,
         name="add/management/staff/"),
    path("login", views.loginPage, name="login"),
    path("logout", views.logoutUser, name="logout"),
    path("", views.index, name="index"),
    path('complaints/documents/<str:filename>',
         views.download_complaint_document, name='download_complaint_document'),

]
