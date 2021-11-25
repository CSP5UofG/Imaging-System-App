from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    context_dict = {}
    return render(request, 'imaging_system_app/index.html', context=context_dict)

def services(request):
    context_dict = {}
    return render(request, 'imaging_system_app/services.html', context=context_dict)
