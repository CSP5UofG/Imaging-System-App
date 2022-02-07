from django.shortcuts import render, redirect
from .models import Customer, Worker, Services, Bill, ProjectBillDetails, ProjectBillBridge, Project, WorkerProjectBridge
import datetime
from imaging_system_app.forms import ServicesForm, CustomerForm, WorkerForm, ProjectForm, WorkerProjectBridgeForm, BillForm, ProjectBillDetailsForm, ProjectBillBridgeForm
from django.urls import reverse



from django.http import HttpResponse

from imaging_system_app.models import Services, Customer, Worker, Project, WorkerProjectBridge, Bill, ProjectBillDetails, ProjectBillBridge

def index(request):
    context_dict = {}
    return render(request, 'imaging_system_app/index.html', context=context_dict)

def services(request):
    context_dict = {}
    
    services = Services.objects.all()
    #services.order_by(service_id) 
    
    # search 'name'
    if request.method == 'POST':
        q = request.POST.get('query')
        if q != "":
            # Allows displaying search string in text box
            context_dict['q']= q
        if q:
            services = Services.objects.filter(name__icontains = q)
            
    
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
    all_projects.order_by("project_date")
    
    # search 'cust_id__cust_name', date filter
    if request.method == 'POST':
        q = request.POST.get('query')
        datefrom = request.POST.get('project_from')
        dateto = request.POST.get('project_to')
        if q != "":
            # Allows displaying search string in text box
            context_dict['q']= q
        if q:
            all_projects = Project.objects.filter(cust_id__cust_name__icontains = q)
        if datefrom != "":
            # Allows displaying search string in text box
            context_dict['datefrom']= datefrom
        if dateto != "":
            # Allows displaying search string in text box
            context_dict['dateto']= dateto
        if datefrom:
            try:
                all_projects  = all_projects.filter(project_date__gte = datetime.date(int(datefrom[0:4]), int(datefrom[4:6]), int(datefrom[6:8])))
            except:
                all_projects  = all_projects.none()
        if dateto:
            try:
                all_projects  = all_projects.filter(project_date__lte = datetime.date(int(dateto[0:4]), int(dateto[4:6]), int(dateto[6:8])))
            except:
                all_projects = all_projects.none()
    

    context_dict['all_projects']= all_projects

    return render(request, 'imaging_system_app/projects.html', context=context_dict)

def customers(request):
    context_dict={}

    customers = Customer.objects.all()
    
    # search 'cust_name', 'cust_tel_no', 'cust_email', 'cust_budget_code'
    if request.method == 'POST':
        q = request.POST.get('query')
        if q != "":
            # Allows displaying search string in text box
            context_dict['q']= q
        if q:
            customers = Customer.objects.filter(Q(cust_name__icontains=q) | Q(cust_tel_no__icontains=q) | Q(cust_email__icontains=q) | Q(cust_budget_code__icontains=q))
        
    customers.order_by("cust_id")

    context_dict['customers']= customers

    return render(request, 'imaging_system_app/customers.html', context=context_dict)
    
def customerDetails(request, cust_id):
    context_dict={}
    context_dict['customer']= Customer.objects.get(cust_id = cust_id)
    context_dict['workers']= Worker.objects.filter(cust_id = cust_id)
    context_dict['projects']= ProjectBillDetails.objects.filter(project_id__cust_id = cust_id)
    context_dict['bills']= Bill.objects.filter(cust_id = cust_id)

    return render(request, 'imaging_system_app/customerdetails.html', context=context_dict)

def editCustomer(request, cust_id):
    context_dict={}
    try:
        customer = Customer.objects.get(cust_id = cust_id)
    except Customer.DoesNotExist:
        customer = None
    
    if customer is None:
        return redirect('/imaging_system_app/')
    
    context_dict['customer']= customer
    #fill new form with current instance
    form = CustomerForm(request.POST or None, instance=customer)
    context_dict['form'] = form
    
    if request.method == 'POST':
        update = CustomerForm(request.POST)
        
        if update.is_valid():
            new_customer = form.save()
            return redirect(reverse('imaging_system_app:customerdetails', kwargs={"cust_id": cust_id}))
    return render(request, 'imaging_system_app/editCustomer.html', context=context_dict)

def editWorker(request, worker_id):
    context_dict={}
    try:
        worker = Worker.objects.get(worker_id = worker_id)
    except Worker.DoesNotExist:
        worker = None
    
    if worker is None:
        return redirect('/imaging_system_app/')
    
    context_dict['worker']= worker
    cust_id = worker.cust_id.cust_id
    #fill new form with current instance
    form = WorkerForm(request.POST or None, instance=worker)
    context_dict['form'] = form
    
    if request.method == 'POST':
        update = WorkerForm(request.POST)
        
        if update.is_valid():
            new_worker = form.save()
            return redirect(reverse('imaging_system_app:customerdetails', kwargs={"cust_id": cust_id}))
    return render(request, 'imaging_system_app/editWorker.html', context=context_dict)

def addCustomer(request):
    form = CustomerForm
    context_dict={'form': form}
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        
        if form.is_valid():
            new_customer = form.save()
            return redirect(reverse('imaging_system_app:customers'))
    return render(request, 'imaging_system_app/addCustomer.html', context=context_dict)


def bills(request):
    context_dict={}

    bills = Bill.objects.all()
    
    # search 'cust_id__cust_name', date filter
    if request.method == 'POST':
        q = request.POST.get('query')
        datefrom = request.POST.get('project_from')
        dateto = request.POST.get('project_to')
        if q != "":
            # Allows displaying search string in text box
            context_dict['q']= q
        if q:
            bills = Bill.objects.filter(cust_id__cust_name__icontains = q)
        if datefrom != "":
            # Allows displaying search string in text box
            context_dict['datefrom']= datefrom
        if dateto != "":
            # Allows displaying search string in text box
            context_dict['dateto']= dateto
        if datefrom:
            try:
                bills = bills.filter(project_date__gte = (datetime.dateint(datefrom[0:4]), int(datefrom[4:6]), int(datefrom[6:8])))
            except:
                bills = bills.none()
        if dateto:
            try:
                bills = bills.filter(project_date__lte = datetime.date(int(dateto[0:4]), int(dateto[4:6]), int(dateto[6:8])))
            except:
                bills = bills.none()
                
    bills.order_by("bill_id")

    context_dict['bills']= bills

    return render(request, 'imaging_system_app/bills.html', context=context_dict)
    
def queries(request):
    # sample view for queries in imaging_system_app/queries/
    context_dict={}
    projects = Project.objects.all()
    if request.method == 'POST':
        query = request.POST.get('project_customer')
        datefrom = request.POST.get('project_from')
        dateto = request.POST.get('project_to')
        if query != "":
            # Allows displaying search string in text box
            context_dict['query']= query
        if query:
            projects = Project.objects.filter(cust_id__cust_name__icontains = query)
            
        if datefrom != "":
            # Allows displaying search string in text box
            context_dict['datefrom']= datefrom
        if dateto != "":
            # Allows displaying search string in text box
            context_dict['dateto']= dateto
        if datefrom:
            try:
                projects = projects.filter(project_date__gte = datetime.date(int(datefrom[0:4]), int(datefrom[4:6]), int(datefrom[6:8])))
            except:
                projects = projects.none()
        if dateto:
            try:
                projects = projects.filter(project_date__lte = datetime.date(int(dateto[0:4]), int(dateto[4:6]), int(dateto[6:8])))
            except:
                projects = projects.none()
        
        
    context_dict['projects']= projects
    return render(request, 'imaging_system_app/queries.html', context=context_dict)