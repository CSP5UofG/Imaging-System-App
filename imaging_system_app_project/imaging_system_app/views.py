from django.shortcuts import render, redirect
from .models import Customer, Worker, Services, Bill, ProjectBillDetails, ProjectBillBridge, Project, WorkerProjectBridge
import datetime
from imaging_system_app.forms import ServicesForm, CustomerForm, WorkerForm, ProjectForm, WorkerProjectBridgeForm, BillForm, ProjectBillDetailsForm, ProjectBillBridgeForm
from django.urls import reverse
from django.http import HttpResponse

from django_xhtml2pdf.utils import generate_pdf

from imaging_system_app.models import Services, Customer, Worker, Project, WorkerProjectBridge, Bill, ProjectBillDetails, ProjectBillBridge


def index(request):
    context_dict = {}
    context_dict['projects'] = Project.objects.order_by('-project_date')[:5]
    context_dict['bills'] = Bill.objects.order_by('-billing_date')[:5]
    return render(request, 'imaging_system_app/index.html', context=context_dict)

# ===================== SERVICES =====================  #

def services(request):
    context_dict = {}
    
    services = Services.objects.all()
    #TODO: Implement sorting based on Service ID
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

def editService(request, id):
    #find the walk object to edit
    try:
        service = Services.objects.filter(service_id = id).first()
    except Services.DoesNotExist:
        service = None
    
    if service is None:
        return redirect('/imaging_system_app/')
    
    #fill new form with current instance
    form = ServicesForm(request.POST or None, instance=service)
    context_dict ={'form': form, 'id': id}
    
    if request.method == 'POST':
        update = ServicesForm(request.POST)
        
        if form.is_valid():
            new_service = form.save(commit = False)
            new_service.in_house_price = (new_service.normal_price)/2
            new_service.outside_price = (new_service.normal_price)*1.5
            new_service.save()
            return redirect(reverse('imaging_system_app:services'))
    return render(request, 'imaging_system_app/editServices.html', context=context_dict)

# ===================== PROJECTS =====================  #

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

def projectDetails(request, id):
    context_dict={}
    context_dict['project'] = ProjectBillDetails.objects.get(project_id = id)
    context_dict['workers'] = WorkerProjectBridge.objects.filter(project_id = id)
    return render(request, 'imaging_system_app/projectDetails.html', context=context_dict)

"""def addProject(request):
    form = ProjectForm
    context_dict={'form': form}
    
    if request.method == 'POST':
        form = ProjectForm(request.POST)
        
        if form.is_valid():
            new_project = form.save()
            return redirect(reverse('imaging_system_app:projects'))
    return render(request, 'imaging_system_app/addProject.html', context=context_dict)
"""
def addProject(request):
    context_dict = {}
    
    customerform = CustomerForm
    workerform = WorkerForm
    projectform = ProjectForm
    projectbilldetailsform = ProjectBillDetailsForm
    
    context_dict['customerform'] = customerform
    context_dict['workerform'] = workerform
    context_dict['projectform'] = projectform
    context_dict['projectbilldetailsform'] = projectbilldetailsform
    
    if request.method == 'POST':
        customerform = CustomerForm(request.POST)
        workerform = WorkerForm(request.POST)
        projectform = ProjectForm(request.POST)
        projectbilldetailsform = ProjectBillDetailsForm(request.POST)
        
        worker = workerform.instance
        project = projectform.instance
        projectbilldetails = projectbilldetailsform.instance
        
        if customerform.is_valid():
            customer = customerform.save()
            
            # add customer to Worker object
            worker.cust_id = customer
            # add customer to Project object
            project.cust_id = customer
            if workerform.is_valid():
                worker.save()
                if projectform.is_valid():
                    project.save()
                    # add project and worker to WorkerProjectBridge
                    WorkerProjectBridge.objects.create(worker_id=worker, project_id=project)
                    # add project to ProjectBillDetails object
                    projectbilldetails.project_id = project
                    if projectbilldetailsform.is_valid():
                        projectbilldetails.get_total()
                        projectbilldetails.save()
                        return redirect(reverse('imaging_system_app:projects'))
    return render(request, 'imaging_system_app/addProject.html', context=context_dict)

def editProject(request, id):
    context_dict={}
    try:
        project = ProjectBillDetails.objects.get(project_id = id)
        context_dict['project'] = project
        worker = WorkerProjectBridge.objects.filter(project_id = id).first().worker_id
        context_dict['workers'] = worker
    except ProjectBillDetails.DoesNotExist:
        project = None
    
    if project is None:
        return redirect('/imaging_system_app/')
        
    #fill new form with current instance
    customerform = CustomerForm(request.POST or None, instance=project.project_id.cust_id)
    workerform = WorkerForm(request.POST or None, instance=worker)
    projectform = ProjectForm(request.POST or None, instance=project.project_id)
    projectbilldetailsform = ProjectBillDetailsForm(request.POST or None, instance=project)
    context_dict['customerform'] = customerform
    context_dict['workerform'] = workerform
    context_dict['projectform'] = projectform
    context_dict['projectbilldetailsform'] = projectbilldetailsform
    context_dict['id'] = id
    
    if request.method == 'POST':
        customerupdate = CustomerForm(request.POST)
        workerupdate = WorkerForm(request.POST)
        projectupdate = ProjectForm(request.POST)
        projectbilldetailsupdate = ProjectBillDetailsForm(request.POST)
    
        
        if customerupdate.is_valid() and workerupdate.is_valid() and projectupdate.is_valid() and projectbilldetailsupdate.is_valid():
            customerupdate.save()
            workerupdate.save()
            projectform.save()
            projectbilldetailsform.save()
            return redirect(reverse('imaging_system_app:project-details', kwargs={"project_id": id}))
    return render(request, 'imaging_system_app/editProject.html', context=context_dict)

# ===================== CUSTOMERS =====================  #

def customers(request):
    context_dict={}

    customers = Customer.objects.all()
    customers.order_by("cust_id")

    context_dict['customers']= customers

    return render(request, 'imaging_system_app/customers.html', context=context_dict)

def customerDetails(request, id):
    context_dict={}
    context_dict['customer']= Customer.objects.get(cust_id = id)
    context_dict['workers']= Worker.objects.filter(cust_id = id)
    context_dict['projects']= ProjectBillDetails.objects.filter(project_id__cust_id = id)
    context_dict['bills']= Bill.objects.filter(cust_id = id)

    return render(request, 'imaging_system_app/customerDetails.html', context=context_dict)


def addCustomer(request):
    form = CustomerForm
    context_dict={'form': form}
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        
        if form.is_valid():
            new_customer = form.save()
            return redirect(reverse('imaging_system_app:customers'))
    return render(request, 'imaging_system_app/addCustomer.html', context=context_dict)

def editCustomer(request, id):
    #find the walk object to edit
    try:
        customer = Customer.objects.filter(cust_id = id).first()
    except Customer.DoesNotExist:
        customer = None
    
    if customer is None:
        return redirect('/imaging_system_app/')
    
    #fill new form with current instance
    form = CustomerForm(request.POST or None, instance=customer)
    context_dict ={'form': form, 'id': id}
    
    if request.method == 'POST':
        update = CustomerForm(request.POST)
        
        if update.is_valid():
            new_customer = form.save()
            return redirect(reverse('imaging_system_app:customers'))
    return render(request, 'imaging_system_app/editCustomer.html', context=context_dict)

# ===================== WORKER =====================  #

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
            return redirect(reverse('imaging_system_app:customer-details', kwargs={"cust_id": cust_id}))
    return render(request, 'imaging_system_app/editWorker.html', context=context_dict)

# ===================== BILLS =====================  #

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

def billDetails(request, id):
    context_dict = bill_context_dict(id)
    # TODO: combine bill units and calculate grand total
    return render(request, 'imaging_system_app/billDetails.html', context=context_dict)
    
def printBill(request, id):
    context_dict = bill_context_dict(id)
    
    resp = HttpResponse(content_type='application/pdf')
    result = generate_pdf('imaging_system_app/bill_pdf.html', file_object=resp, context = context_dict)
    return result
    
def bill_context_dict(bill_id):
    # Helper function to create context_dict for bill
    context_dict = {}
    context_dict['bill'] = Bill.objects.get(bill_id=bill_id)
    projectbillbridge = ProjectBillBridge.objects.filter(bill_id=bill_id)
    projectbilldetails = ProjectBillDetails.objects.filter(project_bill_id__in=projectbillbridge.values('project_bill_id'))
    context_dict['projectbilldetails'] = projectbilldetails
    projects = Project.objects.filter(project_id__in=projectbilldetails.values('project_id'))
    workerprojectbridge = WorkerProjectBridge.objects.filter(project_id__in=projects.values('project_id'))
    workers = Worker.objects.filter(worker_id__in=workerprojectbridge.values('worker_id'))
    context_dict['workers'] = workers
    context_dict['start_date'] = projects.order_by('project_date').first().project_date
    context_dict['end_date'] = projects.order_by('project_date').last().project_date
    return context_dict    

# ===================== QUERIES =====================  #

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
