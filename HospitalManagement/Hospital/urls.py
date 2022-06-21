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
    path('admin-doctor-record', admin_doctor_record_view,name='admin-record-doctor'),
    path('admin-doctor-add', admin_doctor_add_view,name='admin_doctor_add_view'),
    path('admin-doctor-approve', admin_doctor_approve_view,name='admin-doctor-approve'),
    path('admin-approve-doctor/<int:pk>', admin_approve_doctor_view,name='admin-approve-doctor'),
    path('admin-doctor-reject/<int:pk>',admin_reject_doctor_view,name='admin-doctor-reject'),

















    path('doctor-dashoard',doctor_dashoard_view,name='doctor-dashoard'),
    path('doctor-view-patient',doctor_view_patient,name='doctor-view-patient'),
    path('doctor-view-appointment',doctor_view_appointment,name='doctor-view-appointment'),
    path('delete-appointment/<int:pk>', delete_appointment_view,name='delete-appointment'),

    
]