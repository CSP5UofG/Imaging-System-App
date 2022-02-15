from django.shortcuts import render, redirect
from imaging_system_app.models import Customer, Worker, Services, Bill, ProjectServicesBridge, ProjectBillBridge, Project, WorkerProjectBridge
import datetime
from imaging_system_app.forms import ServicesForm, CustomerForm, WorkerForm, ProjectForm, WorkerProjectBridgeForm, BillForm, ProjectServicesBridgeForm, ProjectBillBridgeForm
from django.urls import reverse
from django.http import HttpResponse

from django_xhtml2pdf.utils import generate_pdf

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
                all_projects  = all_projects.filter(project_date__gte = datetime.date(int(datefrom[4:8]), int(datefrom[2:4]), int(datefrom[0:2])))
            except:
                all_projects  = all_projects.none()
        if dateto:
            try:
                all_projects  = all_projects.filter(project_date__lte = datetime.date(int(dateto[4:8]), int(dateto[2:4]), int(dateto[0:2])))
            except:
                all_projects = all_projects.none()
    

    context_dict['all_projects']= all_projects

    return render(request, 'imaging_system_app/projects.html', context=context_dict)

def projectDetails(request, id):
    context_dict={}
    context_dict['project'] = Project.objects.get(project_id = id)
    context_dict['services'] = ProjectServicesBridge.objects.filter(project_id = id)
    context_dict['workers'] = WorkerProjectBridge.objects.filter(project_id = id)
    return render(request, 'imaging_system_app/projectDetails.html', context=context_dict)
    
def addProject(request):
    context_dict = {}
    
    customerform = CustomerForm
    workerform = WorkerForm
    projectform = ProjectForm
    projectservicesbridgeform = ProjectServicesBridgeForm
    
    context_dict['customerform'] = customerform
    context_dict['workerform'] = workerform
    context_dict['projectform'] = projectform
    context_dict['projectservicesbridgeform'] = projectservicesbridgeform
    
    if request.method == 'POST':
        customerform = CustomerForm(request.POST)
        workerform = WorkerForm(request.POST)
        projectform = ProjectForm(request.POST)
        projectservicesbridgeform = ProjectServicesBridgeForm(request.POST)
        
        if customerform.is_valid() and workerform.is_valid() and projectform.is_valid() and projectservicesbridgeform.is_valid():
            customer = customerform.save()
            worker = workerform.save(commit = False)
            project = projectform.save(commit = False)
            projectservicesbridge = projectservicesbridgeform.save(commit = False)
            
            # add customer to Worker object
            worker.cust_id = customer
            worker.save()
            # add customer to Project object
            project.cust_id = customer
            project.save()
            # add project to ProjectServicesBridge object
            projectservicesbridge.project_id = project
            projectservicesbridge.save()
            # add project and worker to WorkerProjectBridge
            WorkerProjectBridge.objects.create(worker_id=worker, project_id=project)
            # calculate cost of project and its services
            calculate_project(project, customer.cust_type)
            return redirect(reverse('imaging_system_app:projects'))
    return render(request, 'imaging_system_app/addProject.html', context=context_dict)
    

def editProject(request, id):
    context_dict={}
    try:
        project = Project.objects.get(project_id = id)
        context_dict['project'] = project
        projectservicesbridge = ProjectServicesBridge.objects.filter(project_id = id).first()
        worker = WorkerProjectBridge.objects.filter(project_id = id).first().worker_id
        context_dict['workers'] = worker
    except Project.DoesNotExist:
        project = None
    
    if project is None:
        return redirect('/imaging_system_app/')
        
    #fill new form with current instance
    customerform = CustomerForm(request.POST or None, instance=project.cust_id)
    workerform = WorkerForm(request.POST or None, instance=worker)
    projectform = ProjectForm(request.POST or None, instance=project)
    projectservicesbridgeform = ProjectServicesBridgeForm(request.POST or None, instance=projectservicesbridge)
    context_dict['customerform'] = customerform
    context_dict['workerform'] = workerform
    context_dict['projectform'] = projectform
    context_dict['projectservicesbridgeform'] = projectservicesbridgeform
    context_dict['id'] = id
    
    if request.method == 'POST':
        if customerform.is_valid() and workerform.is_valid() and projectform.is_valid() and projectservicesbridgeform.is_valid():
            customerform.save()
            workerform.save()
            projectform.save()
            projectservicesbridgeform.save()
            calculate_costs(project)
            return redirect(reverse('imaging_system_app:project-details', kwargs={"id": id}))
    return render(request, 'imaging_system_app/editProject.html', context=context_dict)


# ===================== CUSTOMERS =====================  #

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
    
def customerDetails(request, id):
    context_dict={}
    context_dict['customer']= Customer.objects.get(cust_id = id)
    context_dict['workers']= Worker.objects.filter(cust_id = id)
    context_dict['projects']= Project.objects.filter(cust_id__cust_id = id)
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
    
    context_dict = {'customer': customer}
    #fill new form with current instance
    form = CustomerForm(request.POST or None, instance=customer)
    context_dict['form'] = form
    context_dict['id'] = id
    
    if request.method == 'POST':
        update = CustomerForm(request.POST)
        
        if update.is_valid():
            new_customer = form.save()
            return redirect(reverse('imaging_system_app:customer-details', kwargs={"id": id}))
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
                bills = bills.filter(project_date__gte = (datetime.dateint(datefrom[4:8]), int(datefrom[2:4]), int(datefrom[0:2])))
            except:
                bills = bills.none()
        if dateto:
            try:
                bills = bills.filter(project_date__lte = datetime.date(int(dateto[4:8]), int(dateto[2:4]), int(dateto[0:2])))
            except:
                bills = bills.none()
                
    bills.order_by("bill_id")

    context_dict['bills']= bills

    return render(request, 'imaging_system_app/bills.html', context=context_dict)

def billDetails(request, id):
    context_dict = bill_context_dict(id)
    # TODO: combine bill units and calculate grand total
    return render(request, 'imaging_system_app/billDetails.html', context=context_dict)

def addBill(request):
    context_dict = {}
    billform = BillForm
    projectbillbridgeform = ProjectBillBridgeForm
    context_dict['billform'] = billform
    context_dict['projectbillbridgeform'] = ProjectBillBridgeForm
    
    if request.method == 'POST':
        billform = BillForm(request.POST)
        projectbillbridgeform = ProjectBillBridgeForm(request.POST)
        
        if billform.is_valid() and projectbillbridgeform.is_valid():
            bill = billform.save()
            projectbillbridge = projectbillbridgeform.save(commit = False)
            projectbillbridge.bill_id = bill
            projectbillbridge.save()
            calculate_bill(bill)
            return redirect(reverse('imaging_system_app:bills'))
    return render(request, 'imaging_system_app/addBill.html', context=context_dict)
    
def editBill(request, id):
    context_dict={}
    try:
        bill = Bill.objects.get(bill_id = id)
        context_dict['bill'] = bill
    except Bill.DoesNotExist:
        bill = None
    
    if bill is None:
        return redirect('/imaging_system_app/')
        
    #fill new form with current instance
    billform = BillForm(request.POST or None, instance=bill)
    context_dict['billform'] = billform
    context_dict['id'] = id
    
    if request.method == 'POST':
        if billform.is_valid():
            billform.save()
            calculate_bill(bill)
            return redirect(reverse('imaging_system_app:bill-details', kwargs={"id": id}))
    return render(request, 'imaging_system_app/editBill.html', context=context_dict)

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
    projects = Project.objects.filter(project_id__in=projectbillbridge.values('project_id'))
    context_dict['projects'] = projects
    services = ProjectServicesBridge.objects.filter(project_id__in=projects.values('project_id')).order_by('service_id', 'project_id__project_id')
    context_dict['services'] = services
    
    workerprojectbridge = WorkerProjectBridge.objects.filter(project_id__in=projects.values('project_id'))
    workers = list(Worker.objects.filter(worker_id__in=workerprojectbridge.values('worker_id')).values_list('worker_name', flat=True).distinct())
    context_dict['workers'] = workers
    context_dict['start_date'] = projects.order_by('project_date').first().project_date
    context_dict['end_date'] = projects.order_by('project_date').last().project_date
    
    return context_dict    

# ===================== COST CALCULATION =====================  #
def calculate_service(projectservicesbridge, discount):
    cost = float(discount) * float(projectservicesbridge.service_id.normal_price) * float(projectservicesbridge.units)
    projectservicesbridge.cost = cost
    projectservicesbridge.save()
    return cost

def calculate_project(project, discount):
    tot = 0
    projectservicesbridge = ProjectServicesBridge.objects.filter(project_id=project.project_id)
    services = Services.objects.filter(service_id__in=projectservicesbridge.values('service_id'))
    for pss in projectservicesbridge:
        cost = calculate_service(pss, discount)
        tot += cost
    project.total = tot
    project.save()
    
def calculate_bill(bill):
    tot = 0
    projectbillbridge = ProjectBillBridge.objects.filter(bill_id=bill.bill_id)
    for pbb in projectbillbridge:
        tot += pbb.project_id.total
    if bill.extra1_cost:
        tot += bill.extra1_cost
    if bill.extra2_cost:
        tot += bill.extra2_cost
    bill.total_cost = tot
    bill.save()
    
def calculate_costs(project):
    discount = project.cust_id.cust_type
    # adjust cost of the project
    calculate_project(project, discount)
    bill = ProjectBillBridge.objects.get(project_id=project.project_id).bill_id
    projectbillbridge = ProjectBillBridge.objects.filter(bill_id=bill.bill_id)
    bills = []
    for pbb in projectbillbridge:
        # adjust projects in the same bill
        calculate_project(pbb.project_id, discount)
        if pbb.bill_id not in bills:
            bills.append(pbb.bill_id)
    for bill in bills:
        # adjust cost of bills the project is in
        calculate_bill(bill)
    
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
