from django.shortcuts import render, redirect
from imaging_system_app.models import Customer, Worker, Services, Bill, ProjectServicesBridge, ProjectBillBridge, Project, WorkerProjectBridge
from imaging_system_app.forms import UserForm, ServicesForm, CustomerForm, WorkerForm, ProjectForm, WorkerProjectBridgeForm, BillForm, ProjectServicesBridgeForm
from django.urls import reverse
from django.http import HttpResponse
from django.db.models import Q
from django.forms import formset_factory
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django_xhtml2pdf.utils import generate_pdf
from write_excel import create_excel
from create_statistics_plots import create_plots
import datetime

# ===================== USER AUTHENTICATION =====================  #

def register(request):
    """
    Display form for user registration.

    **Context**

    ``user_form``
        The UserForm for creating an instance of :model:`auth.User`.
    ``registered``
        Boolean value that becomes True when user_form is valid.

    **Template:**

    :template:`imaging_system_app/register.html`
    """
    registered = False
    
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.is_active = False
            user.save()
            registered = True
    else:
        user_form = UserForm()
    
    return render(request, 'imaging_system_app/register.html',
                  context = {'user_form': user_form, 
                             'registered': registered})

def user_login(request):
    """
    Display form for user login.
    
    User is redirected to :template:`imaging_system_app/index.html` when login is successful.

    **Template:**

    :template:`imaging_system_app/login.html`
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('imaging_system_app:index'))
        else:
            return HttpResponse("You have either entered invalid login details or your account has not been activated yet.")
    else:
        return render(request, 'imaging_system_app/login.html')

@login_required
def user_logout(request):
    """User is logged out and redirected to :template:`imaging_system_app/login.html`."""
    logout(request)
    return redirect(reverse('imaging_system_app:login'))

# ===================== HOME PAGE =====================  #

@login_required
def index(request):
    """
    Home page of the app.
    
    Displays the 5 most recent instances of :model:`imaging_system_app.Project` by project_date.
    
    Displays the 5 most recent instances of :model:`imaging_system_app.Bill` by billing_date.
    
    **Context**

    ``projects``
        The 5 most recent instances of :model:`imaging_system_app.Project` by project_date.
    ``bills``
        The 5 most recent instances of :model:`imaging_system_app.Bill` by billing_date.

    **Template:**

    :template:`imaging_system_app/index.html`
    """
    context_dict = {}
    context_dict['projects'] = Project.objects.order_by('-project_date')[:5]
    context_dict['bills'] = Bill.objects.order_by('-billing_date')[:5]
    return render(request, 'imaging_system_app/index.html', context=context_dict)


# ===================== SERVICES =====================  #

@login_required
def services(request):
    """
    Services
    
    Display all existing instances of :model:`imaging_system_app.Services`.  
    
    Search functionality for the name of :model:`imaging_system_app.Services`.

    **Context**

    ``services``
        All instances of :model:`imaging_system_app.Services`.
    ``query``
        User input for searching the name of :model:`imaging_system_app.Services`.  

    **Template:**

    :template:`imaging_system_app/services.html`
    """
    context_dict = {}
    
    services = Services.objects.all()
    
    # search 'name'
    if request.method == 'POST':
        query = request.POST.get('service_name')
        if query != "":
            # Allows displaying search string in text box
            context_dict['query']= query
        if query:
            services = Services.objects.filter(name__icontains = query)
    
    context_dict['services']= services

    return render(request, 'imaging_system_app/services.html', context=context_dict)

@login_required
def addService(request):
    """
    Add Service
    
    Display the ServicesForm for creating a new instance of :model:`imaging_system_app.Services`.
    
    The external_price of the service is calculated and saved.
    
    The user is redirected to :template:`imaging_system_app/Services.html` after submission.

    **Context**

    ``form``
        The ServicesForm for creating an instance of :model:`imaging_system_app.Services`.

    **Template:**

    :template:`imaging_system_app/addServices.html`
    """
    form = ServicesForm
    context_dict={'form': form}
    
    if request.method == 'POST':
        form = ServicesForm(request.POST)
        
        if form.is_valid():
            new_service = form.save(commit = False)
            new_service.external_price = (new_service.normal_price)*1.5
            new_service.save()
            return redirect(reverse('imaging_system_app:services'))
    return render(request, 'imaging_system_app/addServices.html', context=context_dict)

@login_required
def editService(request, id):
    """
    Edit Service
    
    Display the ServicesForm for editing an instance of :model:`imaging_system_app.Services` with a matching service_id to the keyword argument id.
    
    The external_price of the service is calculated and saved.
    
    The user is redirected to :template:`imaging_system_app/index.html` if the instance of :model:`imaging_system_app.Services` is not found.
    
    The user is redirected to :template:`imaging_system_app/services.html` after submission.
    
    **Keyword arguments**

    ``id``
        The service_id of an instance of :model:`imaging_system_app.Services`.

    **Context**

    ``form``
        The filled in ServicesForm for editing the instance of :model:`imaging_system_app.Services`.
    ``id``
        The keyword argument id.

    **Template:**

    :template:`imaging_system_app/editServices.html`
    """
    try:
        service = Services.objects.get(service_id = id)
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
            new_service.external_price = (new_service.normal_price)*1.5
            new_service.save()
            return redirect(reverse('imaging_system_app:services'))
    return render(request, 'imaging_system_app/editServices.html', context=context_dict)

# ===================== PROJECTS =====================  #

@login_required
def projects(request):
    """
    Projects
    
    Display all existing instances of :model:`imaging_system_app.Project`.  
    
    Search functionality for the cust_name of :model:`imaging_system_app.Customer` associated with an instance of :model:`imaging_system_app.Project`.  
    
    Filter functionality, date from and date to, for the project_date of all instances of :model:`imaging_system_app.Project`. 

    **Context**

    ``projects``
        All instances of :model:`imaging_system_app.Project`.
    ``query``
        User input for searching the cust_name of :model:`imaging_system_app.Customer` associated with an instance of :model:`imaging_system_app.Project`.  
    ``datefrom``
        User input for filter start date for the project_date of all instances of :model:`imaging_system_app.Project`.
    ``dateto``
        User input for filter end date for the project_date of all instances of :model:`imaging_system_app.Project`.

    **Template:**

    :template:`imaging_system_app/projects.html`
    """
    context_dict={}
    projects = Project.objects.all().order_by('-project_date', '-project_id')
    if request.method == 'POST':
        query = request.POST.get('project_customer')
        datefrom = request.POST.get('project_from')
        dateto = request.POST.get('project_to')
        if query != "":
            # Allows displaying search string in text box
            context_dict['query']= query
        if query:
            projects = Project.objects.filter(cust_id__cust_name__icontains = query).order_by('-project_date', '-project_id')
            
        if datefrom != "":
            # Allows displaying search string in text box
            context_dict['datefrom']= datefrom
        if dateto != "":
            # Allows displaying search string in text box
            context_dict['dateto']= dateto
        if datefrom:
            try:
                
                projects = projects.filter(project_date__gte = datefrom).order_by('-project_date', '-project_id')
            except:
                projects = projects.none()
        if dateto:
            try:
                projects = projects.filter(project_date__lte = dateto).order_by('-project_date', '-project_id')
            except:
                projects = projects.none()
        
        
    context_dict['projects']= projects
    return render(request, 'imaging_system_app/projects.html', context=context_dict)

@login_required
def projectdetails(request, id):
    """
    Project Details
    
    Display an individual :model:`imaging_system_app.Project`.
    
    **Keyword arguments**

    ``id``
        The project_id of an instance of :model:`imaging_system_app.Project`.

    **Context**

    ``project``
        An instance of :model:`imaging_system_app.Project` matching the keyword argument id.
    ``services``
        All instances of :model:`imaging_system_app.Services` associated with project.
    ``workers``
        All instances of :model:`imaging_system_app.Worker` associated with project.

    **Template:**

    :template:`imaging_system_app/projectdetails.html`
    """
    context_dict={}
    context_dict['project'] = Project.objects.get(project_id = id)
    context_dict['services'] = ProjectServicesBridge.objects.filter(project_id = id)
    context_dict['workers'] = WorkerProjectBridge.objects.filter(project_id = id)
     
    return render(request, 'imaging_system_app/projectdetails.html', context=context_dict)


@login_required    
def addProject(request):
    """
    Add Project
    
    Display the ProjectForm and ProjectServicesBridgeForm for creating a new instance of :model:`imaging_system_app.Project` and instances of :model:`imaging_system_app.ProjectServicesBridge`.
        
    The instance of :model:`imaging_system_app.Project` and associated instances of :model:`imaging_system_app.Worker` are used to create instances of :model:`imaging_system_app.WorkerProjectBridge`.
    
    The cost of the project is calculated.
    
    The user is redirected to :template:`imaging_system_app/Projects.html` after submission.

    **Context**

    ``projectform``
        The ProjectForm for creating an instance of :model:`imaging_system_app.Project`.
    ``projectservicesbridgeform``
        The ProjectServicesBridgeForm for creating an instance of :model:`imaging_system_app.ProjectServicesBridge`.
    ``all_customer``
        All instances of :model:`imaging_system_app.Customer`.

    **Template:**

    :template:`imaging_system_app/addProject.html`
    """
    context_dict = {}
    
    projectform = ProjectForm
    projectservicesbridgeFormSet=formset_factory(ProjectServicesBridgeForm)
    customers = Customer.objects.all().order_by('cust_name')
    
    context_dict['projectform'] = projectform
    context_dict['all_customer'] = customers
    context_dict['projectservicesbridgeformset'] = projectservicesbridgeFormSet
        
    if request.method == 'POST':
        customer = Customer.objects.get(cust_id = request.POST['customer_id'])
        workers = Worker.objects.filter(pk__in = request.POST.getlist('worker_id'))

        projectform = ProjectForm(request.POST)
        PSBformset = projectservicesbridgeFormSet(request.POST)
        
        if projectform.is_valid() and PSBformset.is_valid():
            project = projectform.save(commit = False)
            project.cust_id = customer
            project.save()
            
            for PSBform in PSBformset:
                # add project to ProjectServicesBridge object
                projectservicesbridge = PSBform.save(commit = False)
                projectservicesbridge.project_id = project
                projectservicesbridge.save()
            
            for worker in workers:
                # add project and workers to WorkerProjectBridge
                WorkerProjectBridge.objects.create(worker_id=worker, project_id=project)
            # Helper function to remove multiple instances of the same service in the formset
            removeDuplicateServices(project)
            # calculate cost of project and its services
            calculate_project(project, customer.cust_type)
            return redirect(reverse('imaging_system_app:projects'))
    return render(request, 'imaging_system_app/addProject.html', context=context_dict)


def getWorkers(request):
    """
    Get Workers
    
    Display the dropdown menu of :model:`imaging_system_app.Worker` associated with the selected :model:`imaging_system_app.Customer`.

    **Context**
    
    ``workers``
        All instances of :model:`imaging_system_app.Worker` associated with the selected :model:`imaging_system_app.Customer`.

    **Template:**

    :template:`imaging_system_app/worker_dropdown.html`
    """
    customerId = request.GET.get('customer_id')
    workers = Worker.objects.filter(cust_id = customerId).order_by('worker_name')
    context_dict = {'workers': workers}
    return render(request, 'imaging_system_app/worker_dropdown.html', context_dict)
    
def removeDuplicateServices(project):
    """
    Helper function
    
    Check for duplicates in the formset for project services, instances of :model:`imaging_system_app.ProjectServicesBridge` that have the same project_id and service_id.
    
    Only the newest instance is kept, other instances are deleted.
    
    **Keyword arguments**

    ``project``
        The instance of :model:`imaging_system_app.Project` to be checked.
    """
    # Get all services used by the project, sorted by newest first
    services = ProjectServicesBridge.objects.filter(project_id = project).order_by('project_services_bridge_id')
    services_list = []
    delete = []
    for s in services:
        if s.service_id not in services_list:
            # First occurence in the project
            services_list.append(s.service_id)
        else:
            # Service is already in the project, add this instance to the list of isntances to be deleted
            delete.append(s.project_services_bridge_id)
    # Delete the duplicate instances
    ProjectServicesBridge.objects.filter(project_services_bridge_id__in=delete).delete()
        
    
@login_required
def editProject(request, id):
    """
    Edit Project
    
    Display the ProjectForm and ProjectServicesBridgeForm for editing an instance of :model:`imaging_system_app.Project` and instances of :model:`imaging_system_app.ProjectServicesBridge` with a matching project_id to the keyword argument id.
        
    The instance of :model:`imaging_system_app.Project` and associated instances of :model:`imaging_system_app.Worker` are used to update instances of :model:`imaging_system_app.WorkerProjectBridge`.
    
    The cost of the project is recalculated.
    
    The user is redirected to :template:`imaging_system_app/index.html` if the instance of :model:`imaging_system_app.Project` is not found.
    
    The user is redirected to :template:`imaging_system_app/projectdetails.html` after submission.

    
    **Keyword arguments**

    ``id``
        The project_id of an instance of :model:`imaging_system_app.Project`.

    **Context**
    
    ``project``
        The instance of :model:`imaging_system_app.Project`.
    ``worker``
        The first instance of :model:`imaging_system_app.Worker` associated with project.
    ``all_customer``
        All instances of :model:`imaging_system_app.Customer`.
    ``workers``
        All instances of :model:`imaging_system_app.Worker` associated with project.
    ``projectform``
        The filled in ProjectForm for editing the instance of :model:`imaging_system_app.Project`.
    ``projectservicesbridgeform``
        The filled in ProjectServicesBridgeForm for editing the instance of :model:`imaging_system_app.ProjectServicesBridge`.
    ``id``
        The keyword argument id.

    **Template:**

    :template:`imaging_system_app/editProject.html`
    """
    context_dict={}
    try:
        project = Project.objects.get(project_id = id)
        projectservicesbridge = ProjectServicesBridge.objects.filter(project_id = id)
        workerIDs = WorkerProjectBridge.objects.filter(project_id = id).values_list('worker_id', flat=True)
        project_workers = Worker.objects.filter(pk__in = workerIDs).order_by('worker_name')
        customers = Customer.objects.all().order_by('cust_name')
        workers = Worker.objects.filter(cust_id = project.cust_id).order_by('worker_name')
        
        context_dict['project'] = project
        context_dict['project_workers'] = project_workers
        context_dict['all_customer'] = customers
        context_dict['workers'] = workers
    except Project.DoesNotExist:
        project = None
    
    if project is None:
        return redirect('/imaging_system_app/')
        
    #fill new form with current instance
    projectform = ProjectForm(request.POST or None, instance=project)
    all_psb = []
    for psb in projectservicesbridge:
        projectservicesbridgeform = ProjectServicesBridgeForm(request.POST or None, instance=psb)
        all_psb.append(projectservicesbridgeform)
    context_dict['projectform'] = projectform
    context_dict['all_psb'] = all_psb
    context_dict['id'] = id
    
    if request.method == 'POST':

        if projectform.is_valid() and projectservicesbridgeform.is_valid():
            new_worker = Worker.objects.get(worker_id = request.POST['worker_id'])
            modified_customer = Customer.objects.get(cust_id = request.POST['customer_id'])
            
            project_update = projectform.save(commit=False)
            project_update.cust_id = modified_customer
            project_update.save()
            
            projectservicesbridgeform.save()
            
            WorkerProjectBridge.objects.filter(project_id = id).delete()
            WorkerProjectBridge.objects.create(worker_id=new_worker, project_id=project)
            
            # Helper function to remove multiple instances of the same service in the formset
            removeDuplicateServices(project_update)
            
            calculate_costs(project)
            return redirect(reverse('imaging_system_app:project-details', kwargs={"id": id}))
    return render(request, 'imaging_system_app/editProject.html', context=context_dict)


# ===================== CUSTOMERS =====================  #

@login_required
def customers(request):
    """
    Customers
    
    Display all existing instances of :model:`imaging_system_app.Customer`.  
    
    Search functionality for cust_name, cust_tel_no, cust_email and cust_budget_code of :model:`imaging_system_app.Customer`.

    **Context**

    ``customers``
        All instances of :model:`imaging_system_app.Customer`.
    ``query``
        User input for searching the cust_name, cust_tel_no, cust_email and cust_budget_code of :model:`imaging_system_app.Customer`.  

    **Template:**

    :template:`imaging_system_app/customers.html`
    """
    context_dict={}

    customers = Customer.objects.all().order_by('-cust_id')
    
    # search 'cust_name', 'cust_tel_no', 'cust_email', 'cust_budget_code'
    if request.method == 'POST':
        query = request.POST.get('customer_query')
        if query != "":
            # Allows displaying search string in text box
            context_dict['query']= query
        if query:
            customers = Customer.objects.filter(Q(cust_name__icontains=query) | Q(cust_tel_no__icontains=query) | Q(cust_email__icontains=query) | Q(cust_budget_code__icontains=query)).order_by('-cust_id')
        
    customers.order_by("cust_id")

    context_dict['customers']= customers

    return render(request, 'imaging_system_app/customers.html', context=context_dict)

@login_required   
def customerdetails(request, id):
    """
    Customer Details
    
    Display an individual :model:`imaging_system_app.Customer`.
    
    **Keyword arguments**

    ``id``
        The cust_id of an instance of :model:`imaging_system_app.Customer`.

    **Context**

    ``customer``
        An instance of :model:`imaging_system_app.Customer` matching the keyword argument id.
    ``workers``
        All instances of :model:`imaging_system_app.Worker` associated with customer.
    ``projects``
        All instances of :model:`imaging_system_app.Project` associated with customer.
    ``bills``
        All instances of :model:`imaging_system_app.Bill` associated with customer.

    **Template:**

    :template:`imaging_system_app/customerdetails.html`
    """
    context_dict={}
    context_dict['customer']= Customer.objects.get(cust_id = id)
    context_dict['workers']= Worker.objects.filter(cust_id = id).order_by('worker_name')
    context_dict['projects']= Project.objects.filter(cust_id__cust_id = id).order_by('-project_date')
    context_dict['bills']= Bill.objects.filter(cust_id = id).order_by('-billing_date')

    return render(request, 'imaging_system_app/customerdetails.html', context=context_dict)


@login_required
def addCustomer(request):
    """
    Add Customer
    
    Display the CustomerForm for creating a new instance of :model:`imaging_system_app.Customer`.
        
    The user is redirected to :template:`imaging_system_app/customers.html` after submission.

    **Context**

    ``form``
        The CustomerForm for creating an instance of :model:`imaging_system_app.Customer`.

    **Template:**

    :template:`imaging_system_app/addCustomer.html`
    """
    form = CustomerForm
    context_dict={'form': form}
    
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        
        if form.is_valid():
            new_customer = form.save()
            return redirect(reverse('imaging_system_app:customers'))
    return render(request, 'imaging_system_app/addCustomer.html', context=context_dict)

@login_required
def editCustomer(request, id):
    """
    Edit Customer
    
    Display the CustomerForm for editing an instance of :model:`imaging_system_app.Customer` with a matching cust_id to the keyword argument id.
    
    The user is redirected to :template:`imaging_system_app/index.html` if the instance of :model:`imaging_system_app.Customer` is not found.
    
    The user is redirected to :template:`imaging_system_app/customerdetails.html` after submission.
    
    **Keyword arguments**

    ``id``
        The cust_id of an instance of :model:`imaging_system_app.Customer`.

    **Context**

    ``form``
        The filled in CustomerForm for editing the instance of :model:`imaging_system_app.Customer`.
    ``id``
        The keyword argument id.

    **Template:**

    :template:`imaging_system_app/editCustomer.html`
    """
    try:
        customer = Customer.objects.get(cust_id = id)
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
@login_required
def addWorker(request, id):
    """
    Add Worker
    
    Display the WorkerForm for creating an instance of :model:`imaging_system_app.Worker` associated to the instance of :model:`imaging_system_app.Customer` with a matching cust_id to the keyword argument id.
    
    The user is redirected to :template:`imaging_system_app/customers.html` if the instance of :model:`imaging_system_app.Customer` is not found.
    
    The user is redirected to :template:`imaging_system_app/customerdetails.html` after submission.
    
    **Keyword arguments**

    ``id``
        The cust_id of an instance of :model:`imaging_system_app.Customer`.

    **Context**

    ``customer``
        An instance of :model:`imaging_system_app.Customer` matching the keyword argument id.
    ``worker_form``
        The WorkerForm for creating an instance of :model:`imaging_system_app.Worker`.

    **Template:**

    :template:`imaging_system_app/addWorker.html`
    """
    context_dict={}
    try:
        customer = Customer.objects.get(cust_id = id)
    except Customer.DoesNotExist:
        customer = None
    
    if customer is None:
        return redirect(reverse('imaging_system_app:customers'))
        
    worker_form = WorkerForm
    
    context_dict['customer'] = customer
    context_dict['worker_form'] = WorkerForm
    
    if request.method == 'POST':
        worker_form = WorkerForm(request.POST)
        
        if worker_form.is_valid():
            new_worker = worker_form.save(commit=False)
            new_worker.cust_id = customer
            new_worker.save()
            return redirect(reverse('imaging_system_app:customer-details', kwargs={"id": customer.cust_id}))
    return render(request, 'imaging_system_app/addWorker.html', context=context_dict)

 
@login_required
def editWorker(request, id):
    """
    Edit Worker
    
    Display the WorkerForm for editing an instance of :model:`imaging_system_app.Worker` with a matching worker_id to the keyword argument id.
    
    The user is redirected to :template:`imaging_system_app/index.html` if the instance of :model:`imaging_system_app.Worker` is not found.
    
    The user is redirected to :template:`imaging_system_app/customerdetails.html` after submission.
    
    **Keyword arguments**

    ``id``
        The worker_id of an instance of :model:`imaging_system_app.Worker`.

    **Context**

    ``worker``
        An instance of :model:`imaging_system_app.Worker` matching the keyword argument id.
    ``worker_form``
        The filled in WorkerForm for editing the instance of :model:`imaging_system_app.Worker`.

    **Template:**

    :template:`imaging_system_app/editWorker.html`
    """
    context_dict={}
    try:
        worker = Worker.objects.get(worker_id = id)
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
            return redirect(reverse('imaging_system_app:customer-details', kwargs={"id": cust_id}))
    return render(request, 'imaging_system_app/editWorker.html', context=context_dict)

# ===================== BILLS =====================  #

@login_required
def bills(request):
    """
    Bills
    
    Display all existing instances of :model:`imaging_system_app.Bills`.  
    
    Search functionality for the cust_name of :model:`imaging_system_app.Customer` associated with an instance of :model:`imaging_system_app.Bill`.  
    
    Filter functionality, date from and date to, for the billing_date of all instances of :model:`imaging_system_app.Bill`. 

    **Context**

    ``bills``
        All instances of :model:`imaging_system_app.Bill`.
    ``query``
        User input for searching the cust_name of :model:`imaging_system_app.Customer` associated with an instance of :model:`imaging_system_app.Bill`.  
    ``datefrom``
        User input for filter start date for the billing_date of all instances of :model:`imaging_system_app.Bill`.
    ``dateto``
        User input for filter end date for the billing_date of all instances of :model:`imaging_system_app.Bill`.

    **Template:**

    :template:`imaging_system_app/bills.html`
    """
    context_dict={}

    bills = Bill.objects.all().order_by('-billing_date', '-bill_id')
    
    if request.method == 'POST':
        query = request.POST.get('bill_customer')
        datefrom = request.POST.get('bill_from')
        dateto = request.POST.get('bill_to')
        if query != "":
            # Allows displaying search string in text box
            context_dict['query']= query
        if query:
            bills = Bill.objects.filter(cust_id__cust_name__icontains = query).order_by('-billing_date', '-bill_id')
            
        if datefrom != "":
            # Allows displaying search string in text box
            context_dict['datefrom']= datefrom
        if dateto != "":
            # Allows displaying search string in text box
            context_dict['dateto']= dateto
        if datefrom:
            try:
                
                bills = bills.filter(billing_date__gte = datefrom).order_by('-billing_date', '-bill_id')
            except:
                bills = bills.none()
        if dateto:
            try:
                bills = bills.filter(billing_date__lte = dateto).order_by('-billing_date', '-bill_id')
            except:
                bills = bills.none()
                
    bills.order_by("bill_id")

    context_dict['bills']= bills

    return render(request, 'imaging_system_app/bills.html', context=context_dict)

@login_required
def billdetails(request, id):
    """
    Bill details
    
    Display an individual :model:`imaging_system_app.Bill`.
    
    **Keyword arguments**

    ``id``
        The bill_id of an instance of :model:`imaging_system_app.Bill`.

    **Context**

    Uses helper function bill_context_dict.
    
    **Template:**

    :template:`imaging_system_app/billdetails.html`
    """
    context_dict = bill_context_dict(id)
    # TODO: combine bill units and calculate grand total
    return render(request, 'imaging_system_app/billdetails.html', context=context_dict)


@login_required
def addBill(request):
    """
    Add Bill
    
    Display the BillForm for creating a new instance of :model:`imaging_system_app.Bill`.
        
    The instance of :model:`imaging_system_app.Bill` are used to create instances of :model:`imaging_system_app.ProjectBillBridge`.
    
    The cost of the bill is calculated.
    
    The user is redirected to :template:`imaging_system_app/bills.html` after submission.

    **Context**

    ``billform``
        The BillForm for creating an instance of :model:`imaging_system_app.Bill`.
    ``customers``
        All instances of :model:`imaging_system_app.Customer`.

    **Template:**

    :template:`imaging_system_app/addBill.html`
    """
    context_dict = {}
    billform = BillForm
    customers = Customer.objects.all().order_by('cust_name')
    context_dict['billform'] = billform
    context_dict['customers'] = customers
    
    if request.method == 'POST':
        billform = BillForm(request.POST)
        
        if billform.is_valid():
            customer = Customer.objects.get(cust_id = request.POST['customer_id'])
            projects = Project.objects.filter(pk__in = request.POST.getlist('project_id'))
            bill = billform.save(commit=False)
            bill.cust_id = customer
            bill.save()
            for project in projects:
                ProjectBillBridge.objects.create(project_id = project,
                                                 bill_id = bill)
            calculate_bill(bill)
            return redirect(reverse('imaging_system_app:bills'))
    return render(request, 'imaging_system_app/addBill.html', context=context_dict)


def getProjects(request):
    """
    Get Projects
    
    Display the dropdown menu of :model:`imaging_system_app.Project` associated with the selected :model:`imaging_system_app.Customer`.

    **Context**
    
    ``projects``
        All instances of :model:`imaging_system_app.Project` associated with the selected :model:`imaging_system_app.Customer`.

    **Template:**

    :template:`imaging_system_app/project_dropdown.html`
    """
    customerId = request.GET.get('customer_id')
    projects = Project.objects.filter(cust_id = customerId).order_by('-project_date')
    context_dict = {'projects': projects}
    return render(request, 'imaging_system_app/project_dropdown.html', context_dict)
    return render()


@login_required 
def editBill(request, id):
    """
    Edit Bill
    
    Display the BillForm for editing an instance of :model:`imaging_system_app.Bill` with a matching bill_id to the keyword argument id.
        
    The instance of :model:`imaging_system_app.Bill` is used to update instances of :model:`imaging_system_app.ProjectServicesBridge`.
    
    The cost of the bill is recalculated.
    
    The user is redirected to :template:`imaging_system_app/index.html` if the instance of :model:`imaging_system_app.Bill` is not found.
    
    The user is redirected to :template:`imaging_system_app/billdetails.html` after submission.

    
    **Keyword arguments**

    ``id``
        The bill_id of an instance of :model:`imaging_system_app.Bill`.

    **Context**
    
    ``bill``
        The instance of :model:`imaging_system_app.Bill`.
    ``billform``
        The filled in BillForm for editing the instance of :model:`imaging_system_app.Bill`.
    ``id``
        The keyword argument id.

    **Template:**

    :template:`imaging_system_app/editBill.html`
    """
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

@login_required
def printBill(request, id):
    """
    Print Bill
    
    Display the generated PDF bill of the instance of :model:`imaging_system_app.Bill` with a matching bill_id to the keyword argument id.
    
    The default name of the pdf is billing_date_cust_name.pdf
    
    **Keyword arguments**

    ``id``
        The bill_id of an instance of :model:`imaging_system_app.Bill`.

    **Context**
    
    Uses helper function bill_context_dict.

    **Template:**

    :template:`imaging_system_app/bill_pdf.html`
    """
    context_dict = bill_context_dict(id)
    
    # Set pdf file name to date_customer.pdf
    date = str(context_dict['bill'].billing_date)
    cust_name = context_dict['bill'].cust_id.cust_name
    content_disposition = 'inline; filename="' + date + '_' + cust_name + '.pdf"'
    
    resp = HttpResponse(content_type='application/pdf')
    resp['Content-Disposition'] = content_disposition
    result = generate_pdf('imaging_system_app/bill_pdf.html', file_object=resp, context = context_dict)
    return result

def bill_context_dict(bill_id):
    """
    Helper function
    
    Create context_dict for :model:`imaging_system_app.Bill`
    
    **Keyword arguments**

    ``bill_id``
        The bill_id of an instance of :model:`imaging_system_app.Bill`.

    **Context**
    
    ``bill``
        An instance of :model:`imaging_system_app.Bill` matching the keyword argument bill_id.
    ``projects``
        All instances of :model:`imaging_system_app.Project` associated with bill.
    ``services``
        All instances of :model:`imaging_system_app.ProjectServicesBridge` associated with projects.
    ``workers``
        All instances of :model:`imaging_system_app.WorkerProjectBridge` associated with projects.
    ``start_date``
        The project_date of the earliest project.
    ``end_date``
        The project_date of the latest project.
    """
    context_dict = {}
    
    context_dict['bill'] = Bill.objects.get(bill_id=bill_id)
    
    projectbillbridge = ProjectBillBridge.objects.filter(bill_id=bill_id)
    projects = Project.objects.filter(project_id__in=projectbillbridge.values('project_id')).order_by('-project_date')
    context_dict['projects'] = projects
    services = ProjectServicesBridge.objects.filter(project_id__in=projects.values('project_id')).order_by('service_id', 'project_id__project_id')
    context_dict['services'] = services
    
    workerprojectbridge = WorkerProjectBridge.objects.filter(project_id__in=projects.values('project_id'))
    workers = Worker.objects.filter(worker_id__in=workerprojectbridge.values('worker_id')).order_by('worker_name')
    context_dict['workers'] = workers
    context_dict['worker_list'] = list(workers.values_list('worker_name', flat=True).distinct())
    context_dict['start_date'] = projects.order_by('project_date').first().project_date
    context_dict['end_date'] = projects.order_by('project_date').last().project_date
    
    return context_dict    

# ===================== COST CALCULATION =====================  #

def calculate_service(projectservicesbridge, discount):
    """
    Helper function
    
    Calculate and update the cost of an instance of :model:`imaging_system_app.ProjectServicesBridge`.
    
    Returns the cost.
    
    **Keyword arguments**

    ``projectservicesbridge``
        An instance of :model:`imaging_system_app.ProjectServicesBridge`.
    ``discount``
        The cust_type of an instance of :model:`imaging_system_app.Customer`.
    """
    cost = float(discount) * float(projectservicesbridge.service_id.normal_price) * float(projectservicesbridge.units)
    projectservicesbridge.cost = cost
    projectservicesbridge.save()
    return cost

def calculate_project(project, discount):
    """
    Helper function to calculate and update the total of an instance of :model:`imaging_system_app.Project`.
    
    **Keyword arguments**

    ``project``
        An instance of :model:`imaging_system_app.Project`.
    ``discount``
        The cust_type of an instance of :model:`imaging_system_app.Customer`.
    """
    tot = 0
    projectservicesbridge = ProjectServicesBridge.objects.filter(project_id=project.project_id)
    services = Services.objects.filter(service_id__in=projectservicesbridge.values('service_id'))
    for pss in projectservicesbridge:
        cost = calculate_service(pss, discount)
        tot += cost
    project.total = tot
    project.save()
  
def calculate_bill(bill):
    """
    Helper function
    
    Calculate and update the total_cost of an instance of :model:`imaging_system_app.Bill`.
    
    **Keyword arguments**

    ``bill``
        An instance of :model:`imaging_system_app.Bill`.
    """
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
    """
    Main helper function for calculating and updating costs.
    
    Calculate and update the total of an instance of :model:`imaging_system_app.Project`.
    
    Calculate and update the total_cost of instances of :model:`imaging_system_app.Bill` associated to the :model:`imaging_system_app.Project`.
    
    Calculate and update the total of instances of :model:`imaging_system_app.Project` associated to the same :model:`imaging_system_app.Bill`.
    
    **Keyword arguments**

    ``project``
        An instance of :model:`imaging_system_app.Project`.
    """
    discount = project.cust_id.cust_type
    # adjust cost of the project
    calculate_project(project, discount)
    # check if the project is in a bill
    bills = ProjectBillBridge.objects.filter(project_id=project).order_by('-bill_id')
    
    for bill in bills:
        projectbillbridge = ProjectBillBridge.objects.filter(bill_id=bill.bill_id)
        for pbb in projectbillbridge:
            # adjust projects in the same bill
            calculate_project(pbb.project_id, discount)
        # adjust cost of bills the project is in
        calculate_bill(bill.bill_id)


# ===================== STATS =====================  #

@login_required
def viewStatistics(request):
    """
    Create an excel spreadsheet of the database.
    
    Display graphs of statistical data of created instances of :model:`imaging_system_app.Project` and :model:`imaging_system_app.Bill`.

    **Template:**

    :template:`imaging_system_app/statistics.html`
    """
    create_excel()
    create_plots()
    context_dict = {}
    return render(request, 'imaging_system_app/statistics.html', context=context_dict)
