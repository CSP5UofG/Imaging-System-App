from django.shortcuts import render, redirect
from .helper import FieldLookup
from .models import Customer, Worker, Services, Bill, ProjectBillDetails, ProjectBillBridge, Project, WorkerProjectBridge
import datetime
from imaging_system_app.forms import ServicesForm, CustomerForm, WorkerForm, ProjectForm, WorkerProjectBridgeForm, BillForm, ProjectBillDetailsForm, ProjectBillBridgeForm
from django.urls import reverse



from django.http import HttpResponse

from imaging_system_app.models import Services, Customer, Worker, Project, WorkerProjectBridge, Bill, ProjectBillDetails, ProjectBillBridge

def index(request):
    context_dict = {}
    context_dict['projects'] = Project.objects.order_by('-project_date')[:5]
    context_dict['bills'] = Bill.objects.order_by('-billing_date')[:5]
    return render(request, 'imaging_system_app/index.html', context=context_dict)

def services(request):
    context_dict = {}
    
    services = Services.objects.all()
    #services.order_by(service_id) TODO: Implement querying based on Service ID

    context_dict['services']= services

    return render(request, 'imaging_system_app/services.html', context=context_dict)

def addService(request):
    form = ServicesForm
    context_dict={'form': form}
    
    if request.method == 'POST':
        form = ServicesForm(request.POST)
        
        if form.is_valid():
            new_service = form.save(commit = False)
            new_service.in_house_price = (new_service.normal_price)/2
            new_service.outside_price = (new_service.normal_price)*1.5
            new_service.save()
            return redirect(reverse('imaging_system_app:services'))
    return render(request, 'imaging_system_app/addServices.html', context=context_dict)


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

def addCustomer(request):
    form = CustomerForm
    context_dict={'form': form}
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        
        if form.is_valid():
            new_customer = form.save()
            return redirect(reverse('imaging_system_app:customers'))
    return render(request, 'imaging_system_app/addCustomer.html', context=context_dict)

def editCustomer(request):
    #find the walk object to edit
    try:
        customer = Customer.objects.order_by('cust_id')[:1].first()
    except Customer.DoesNotExist:
        customer = None
    
    if customer is None:
        return redirect('/imaging_system_app/')
    
    #fill new form with current instance
    form = CustomerForm(request.POST or None, instance=customer)
    context_dict={'form': form}
    
    if request.method == 'POST':
        update = CustomerForm(request.POST)
        
        if update.is_valid():
            new_customer = form.save()
            return redirect(reverse('imaging_system_app:customers'))
    return render(request, 'imaging_system_app/editCustomer.html', context=context_dict)


def bills(request):
    context_dict={}

    bills = Bill.objects.all()
    bills.order_by("bill_id")

    context_dict['bills']= bills

    return render(request, 'imaging_system_app/bills.html', context=context_dict)