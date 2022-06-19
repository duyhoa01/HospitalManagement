from django import views
from django.contrib import admin
from django.urls import path,include
from .views import *
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('',home_view,name=""),
    path('login', LoginView.as_view(template_name='hospital/login.html'),name='login'),
    
    path('doctorsignup', doctor_signup_view, name='doctorsignup'),
    path('patientsignup', patient_signup_view),

    path('afterlogin', afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='hospital/index.html'),name='logout'),


    path('admin-dashboard',admin_dashboard_view,name='admin-dashboard'),
    path('admin-doctor', admin_doctor_view,name='admin-doctor'),
]