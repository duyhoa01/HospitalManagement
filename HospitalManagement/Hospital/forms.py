from django import forms
from django.contrib.auth.models import User
from .models import *


class AdminSignUpForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }

class DoctorUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class DoctorForm(forms.ModelForm):
    class Meta:
        model=Doctor
        fields=['address','mobile','department','status','profile_pic']

class PatientUserForm(forms.ModelForm):
    class Meta:
        model=User
        fields=['first_name','last_name','username','password']
        widgets = {
        'password': forms.PasswordInput()
        }
class PatientForm(forms.ModelForm):
   
    class Meta:
        model=Patient
        fields=['address','mobile','status','symptoms','profile_pic','assignedDoctor']

class AppointmentForm(forms.ModelForm):
    class Meta:
        model=Appointment
        fields=['doctor','patient','description','status','appointmentDate']