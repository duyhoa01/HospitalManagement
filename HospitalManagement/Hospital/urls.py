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
    path('admin-doctor-record', admin_doctor_record_view,name='admin-doctor-record'),
    path('admin-doctor-add', admin_doctor_add_view,name='admin_doctor_add_view'),
    path('admin-doctor-approve', admin_doctor_approve_view,name='admin-doctor-approve'),
    path('admin-approve-doctor/<int:pk>', admin_approve_doctor_view,name='admin-approve-doctor'),
    path('admin-doctor-reject/<int:pk>',admin_reject_doctor_view,name='admin-doctor-reject'),
    path('admin-update-doctor/<int:pk>', admin_update_doctor_view,name='admin-update-doctor'),
    path('admin-delete-doctor/<int:pk>',admin_delete_doctor_view,name='admin-delete-doctor'),


    path('admin-patient',admin_patient_view,name='admin-patient'),
    path('admin-patient-record',admin_patient_record_view,name='admin-patient-record'),
    path('admin-patient-add',admin_patient_add_view,name='admin-patient-add'),
    path('admin-patient-approve',admin_patient_approve_view,name='admin-patient-approve'),
    path('admin-approve-patient/<int:pk>', admin_approve_patient_view,name='admin-approve-patient'),
    path('admin-reject-patient/<int:pk>', admin_reject_patient_view,name='admin-reject-patient'),
    path('admin-patient-delete/<int:pk>',admin_delete_patientl_view,name='admin-patient-delete'),
    path('admin-update-patient/<int:pk>',admin_update_patient_view,name='admin-update-patient'),

    path('admin-appointment', admin_appointment_view,name='admin-appointment'),
    path('admin-appointment-record', admin_appointment_record_view,name='admin-appointment-record'),
    path('admin-appointment-add', admin_appointment_add_view,name='admin-appointment-add'),
     path('admin-appointment-approve', admin_appointment_approve_view,name='admin-appointment-approve'),
     path('admin-approve-appointment/<int:pk>', admin_approve_appointment_view,name='admin-approve-appointment'),
     path('admin-reject-appointment/<int:pk>', admin_reject_appointment_view,name='admin-reject-appointment'),
]