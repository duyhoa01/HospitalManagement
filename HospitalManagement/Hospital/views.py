from django.shortcuts import render
from django.http import HttpResponseRedirect

# Create your views here.

def home_view(request):
    return render(request,'hospital/index.html')