from django.urls import path
from . import views

urlpatterns = [
    path("register",views.register,name="register"),
    path("login",views.loginPage,name="login"),
    path("logout",views.logoutUser,name="logout"),
    path("index",views.index,name="index"),

    path("faculty",views.faculty,name="faculty"),
]
