
from pickle import TRUE
from django.shortcuts import render, redirect
from django.shortcuts import render, redirect,reverse
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required,user_passes_test
from psutil import users
from . import forms, models
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


# Create your views here.

def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request,'hospital/index.html')

# def login_view(request):
#     return render(request,'hospital/login.html')

def doctor_signup_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        print("ok")
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST,request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor=doctor.save()
           # print(doctor.profile_pic)
            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)
        return HttpResponseRedirect('login')
    return render(request,'hospital/doctor_signup.html',context=mydict)

def patient_signup_view(request):
    userForm=forms.PatientUserForm()
    patientForm=forms.PatientForm()
    mydict={'userForm':userForm,'patientForm':patientForm}
    if request.method=='POST':
        userForm=forms.PatientUserForm(request.POST)
        patientForm=forms.PatientForm(request.POST,request.FILES)
        if userForm.is_valid() and patientForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()
            patient=patientForm.save(commit=False)
            patient.user=user
            patient.assignedDoctorId=request.POST.get('assignedDoctorId')
            patient=patient.save()
            my_patient_group = Group.objects.get_or_create(name='PATIENT')
            my_patient_group[0].user_set.add(user)
        return HttpResponseRedirect('login')
    return render(request,'hospital/patient_signup.html',context=mydict)

def is_admin(user):
    return user.groups.filter(name='ADMIN').exists()
def is_doctor(user):
    return user.groups.filter(name='DOCTOR').exists()
def is_patient(user):
    return user.groups.filter(name='PATIENT').exists()

def afterlogin_view(request):
    if is_admin(request.user):
        return redirect('admin-dashboard')
    elif is_doctor(request.user):
        accountapproval=models.Doctor.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            return redirect('doctor-dashoard')
            # return HttpResponse("Doctor")
        else:
            # return render(request,'hospital/doctor_wait_for_approval.html')
            return HttpResponse("Doctor cho xet")
    elif is_patient(request.user):
        accountapproval=models.Patient.objects.all().filter(user_id=request.user.id,status=True)
        if accountapproval:
            # return redirect('patient-dashboard')
            return HttpResponse("Patient")
        else:
            # return render(request,'hospital/patient_wait_for_approval.html')
            return HttpResponse("Patient Cho Xet")


#-----------------------ADMIN--------------------#

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_dashboard_view(request):
    doctors=models.Doctor.objects.all().order_by('user__date_joined')
    patients=models.Patient.objects.all().order_by('user__date_joined')
    users=models.User.objects.all().order_by('-date_joined')
    roles=[]
    print(users.__len__())
    for u in users:
       roles.append(u.groups.all()[0].name)
       if(u.groups.all()[0].name=='DOCTOR'):
        print(u.doctor)
    print(roles)
    #for three cards
    doctorcount=models.Doctor.objects.all().filter(status=True).count()
    pendingdoctorcount=models.Doctor.objects.all().filter(status=False).count()

    patientcount=models.Patient.objects.all().filter(status=True).count()
    pendingpatientcount=models.Patient.objects.all().filter(status=False).count()

    appointmentcount=models.Appointment.objects.all().filter(status=True).count()
    pendingappointmentcount=models.Appointment.objects.all().filter(status=False).count()
    mydict={
    'roles':roles,
    'users':users,
    'doctors':doctors,
    'patients':patients,
    'doctorcount':doctorcount,
    'pendingdoctorcount':pendingdoctorcount,
    'patientcount':patientcount,
    'pendingpatientcount':pendingpatientcount,
    'appointmentcount':appointmentcount,
    'pendingappointmentcount':pendingappointmentcount,
    }
    return render(request,'hospital/admin_dashboard.html',context=mydict)


@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_view(request):
    return render(request,'hospital/admin_doctor.html')


# DocTOR
@login_required (login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_dashoard_view(request):
    doctor=models.Doctor.objects.filter(user=request.user)
    patientcount=doctor[0].patient_set.filter(status=True).count()
    appointmentcount=doctor[0].appointment_set.filter(status=True).count()
    mydict={
    'patientcount':patientcount,
    'appointmentcount':appointmentcount,
    'doctor':models.Doctor.objects.get(user=request.user), #for profile picture of doctor in sidebar
     }
    return render(request,'hospital/doctor_dashboard.html',context=mydict)










@login_required(login_url='adminlogin')
@user_passes_test(is_doctor)
def doctor_view_patient(request):
    patients=models.Patient.objects.all().filter(status=True,assignedDoctor__user=request.user)
    doctor=models.Doctor.objects.get(user=request.user)
    
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})
   




@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def search_view(request):
    doctor=models.Doctor.objects.get(user_id=request.user.id)
    query=request.GET['query']
    patients=models.Patient.objects.all().filter(status=TRUE,assignedDoctor=request.user.id).filter(Q(symptoms__icontains=query)|Q(user__first_name__icontains=query))
    return render(request,'hospital/doctor_view_patient.html',{'patients':patients,'doctor':doctor})


@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def doctor_view_appointment(request):
    doctor=models.Doctor.objects.filter(user=request.user)
    appointments=doctor[0].appointment_set.filter(status=True)
    
    return render(request,'hospital/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})

@login_required(login_url='doctorlogin')
@user_passes_test(is_doctor)
def delete_appointment_view(request,pk):
    appointment=models.Appointment.objects.get(id=pk)
    appointment.delete()
    doctor=models.Doctor.objects.filter(user=request.user)
    appointments=doctor[0].appointment_set.filter(status=True)
    return render(request,'hospital/doctor_view_appointment.html',{'appointments':appointments,'doctor':doctor})










@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_record_view(request):
    dotors=models.Doctor.objects.all().filter(status=True).order_by('department')
    for d in dotors:
        print(d.user)
    paginator = Paginator(dotors, 4)
  
    pageNumber = request.GET.get('page')
    print(pageNumber)
    try:
        print(0)
        customers = paginator.page(pageNumber)
    except PageNotAnInteger:
        print(1)
        customers = paginator.page(1)
    except EmptyPage:
        print(2)
        customers = paginator.page(paginator.num_pages)
    print(customers)
    # for d in customers:
    #     print(d.user)
    return render(request, 'hospital/admin_doctor_record.html', {'doctors':customers})
    

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_add_view(request):
    userForm=forms.DoctorUserForm()
    doctorForm=forms.DoctorForm()
    mydict={'userForm':userForm,'doctorForm':doctorForm}
    if request.method=='POST':
        userForm=forms.DoctorUserForm(request.POST)
        doctorForm=forms.DoctorForm(request.POST, request.FILES)
        if userForm.is_valid() and doctorForm.is_valid():
            user=userForm.save()
            user.set_password(user.password)
            user.save()

            doctor=doctorForm.save(commit=False)
            doctor.user=user
            doctor.status=True
            doctor.save()

            my_doctor_group = Group.objects.get_or_create(name='DOCTOR')
            my_doctor_group[0].user_set.add(user)

        return HttpResponseRedirect('admin-doctor-record')
    return render(request,'hospital/admin_doctor_register.html',context=mydict)

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_doctor_approve_view(request):
    doctors=models.Doctor.objects.all().filter(status=False)
    return render(request,'hospital/admin_doctor_approve.html',{'doctors':doctors})

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_approve_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    doctor.status=True
    doctor.save()
    return redirect(reverse('admin-doctor-approve'))

@login_required(login_url='adminlogin')
@user_passes_test(is_admin)
def admin_reject_doctor_view(request,pk):
    doctor=models.Doctor.objects.get(id=pk)
    user=models.User.objects.get(id=doctor.user_id)
    user.delete()
    doctor.delete()
    return redirect('admin-doctor-approve')

