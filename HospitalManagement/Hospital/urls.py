from django import views
from django.contrib import admin
from django.urls import path,include
from .views import home_view,doctor_signup_view,patient_signup_view,afterlogin_view
from django.contrib.auth.views import LoginView, LogoutView

urlpatterns = [
    path('',home_view,name=""),
    path('login', LoginView.as_view(template_name='hospital/login.html'),name='login'),
    
    path('doctorsignup', doctor_signup_view, name='doctorsignup'),
    path('patientsignup', patient_signup_view),

    path('afterlogin', afterlogin_view,name='afterlogin'),
    path('logout', LogoutView.as_view(template_name='hospital/index.html'),name='logout'),
]