from datetime import datetime
from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Department(models.Model):
    name=models.CharField(max_length=50,null=False)
    description=models.CharField(max_length=255,null=True)

    def __str__(self):
        return "{}".format(self.name)

class Doctor(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic = models.ImageField(upload_to='profile_pic/DoctorProfilePic/',null=True, blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=True)
    department=models.ForeignKey(Department,on_delete=models.CASCADE,blank=False,null=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return "{} ({})".format(self.user.first_name,self.department)

class Patient(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_pic= models.ImageField(upload_to='profile_pic/PatientProfilePic/',null=True,blank=True)
    address = models.CharField(max_length=40)
    mobile = models.CharField(max_length=20,null=False)
    symptoms = models.CharField(max_length=100,null=False)
    assignedDoctor = models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True,blank=True)
    admitDate=models.DateField(auto_now=True)
    status=models.BooleanField(default=False)
    @property
    def get_name(self):
        return self.user.first_name+" "+self.user.last_name
    @property
    def get_id(self):
        return self.user.id
    def __str__(self):
        return self.user.first_name+" ("+self.symptoms+")"

class Appointment(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE,null=True,blank=True)
    doctor=models.ForeignKey(Doctor,on_delete=models.CASCADE,null=True,blank=True)
    appointmentDate=models.DateTimeField(default=datetime.now)
    description=models.TextField(max_length=500)
    status=models.BooleanField(default=False)

    def __str__(self):
        return "{} {}".format(self.patient.user.first_name,self.doctor.user.first_name)





    
