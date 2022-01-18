from django.shortcuts import render

from django.http import HttpResponse

from imaging_system_app.models import Services, Customer, Worker, Project, WorkerProjectBridge, Bill, ProjectBillDetails, ProjectBillBridge

def index(request):
    context_dict = {}
    return render(request, 'imaging_system_app/index.html', context=context_dict)

def services(request):
    context_dict = {}
    
    services = Services.objects.all()
    #services.order_by(service_id) TODO: Implement querying based on Service ID

    context_dict['services']= services

    return render(request, 'imaging_system_app/services.html', context=context_dict)

def projects(request):
    context_dict={}

    
    all_projects = Project.objects.all()
    #all_projects.order_by(project_date)

    context_dict['all_projects']= all_projects

    return render(request, 'imaging_system_app/projects.html', context=context_dict)

def customers(request):
    context_dict={}

    customers = Customer.objects.all()
    customers.order_by("cust_id")

    context_dict['customers']= customers

    return render(request, 'imaging_system_app/customers.html', context=context_dict)

def bills(request):
    context_dict={}

    bills = Bill.objects.all()
    bills.order_by("bill_id")

    context_dict['bills']= bills

    return render(request, 'imaging_system_app/bills.html', context=context_dict)