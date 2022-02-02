from django import forms
from imaging_system_app.models import Customer, Worker, Services, Bill, ProjectBillDetails, ProjectBillBridge, Project, WorkerProjectBridge
from django.utils import timezone


class ServicesForm(forms.ModelForm):
    cust_type = forms.CharField(max_length = 100,
                                help_text = "Customer Type")
    discount = forms.FloatField(help_text = "Discount")
    jeol1200tem_cost = forms.FloatField(help_text = "jeol1200tem cost",
                                        min_value = 0)
    jeol100sem_cost = forms.FloatField(help_text = "jeol100sem cost",
                                       min_value = 0)
    tem_processing_cost = forms.FloatField(help_text = "tem processing cost",
                                           min_value = 0)
    sectioning_stained_cost = forms.FloatField(help_text = "sectioning stained cost",
                                               min_value = 0)
    sectioning_contrast_stained_cost = forms.FloatField(help_text = "sectioning contrast stained cost",
                                                        min_value = 0)
    negative_staining_cost = forms.FloatField(help_text = "negative staining cost",
                                              min_value = 0)
    sem_processing_mounting_cost = forms.FloatField(help_text = "sem processing mounting cost",
                                                    min_value = 0)
    sem_processing_fd_cost = forms.FloatField(help_text = "sem processing fd cost",
                                              min_value = 0)
    sem_cost = forms.FloatField(help_text = "sem cost",
                                min_value = 0)
    immunolabelling_cost = forms.FloatField(help_text = "immunolabelling cost",
                                            min_value = 0)
    cryosectioning_cost = forms.FloatField(help_text = "cryosectioning cost",
                                           min_value = 0)
    freeze_fracture_cost = forms.FloatField(help_text = "freeze fracture cost",
                                            min_value = 0)
    ir_white_cost = forms.FloatField(help_text = "ir white cost",
                                     min_value = 0)
    
    class Meta:
        model = Services
        fields = ('cust_type', 'discount', 'jeol1200tem_cost', 'jeol100sem_cost',
                  'tem_processing_cost', 'sectioning_stained_cost',
                  'sectioning_contrast_stained_cost', 'negative_staining_cost',
                  'sem_processing_mounting_cost', 'sem_processing_fd_cost',
                  'sem_cost', 'immunolabelling_cost', 'cryosectioning_cost',
                  'freeze_fracture_cost', 'ir_white_cost', )


class CustomerForm(forms.ModelForm):
    cust_name = forms.CharField(max_length = 100,
                                help_text = "Customer Name")
    cust_tel_no = forms.CharField(max_length = 11,
                                  help_text = "Customer Tel. no")
    cust_email = forms.CharField(max_length = 100,
                                 help_text = "Customer email address")
    cust_budget_code = forms.IntegerField(help_text = "Budget code",
                                          min_value = 0)
    service_id = forms.ModelChoiceField(queryset = Services.objects.all(),
                                        help_text = "Customer Type")
    
    class Meta:
        model = Customer
        fields = ('cust_name', 'cust_tel_no', 'cust_email', 'cust_budget_code',
                  'service_id', )


class WorkerForm(forms.ModelForm):
    worker_name = forms.CharField(max_length = 100,
                                  help_text = "Worker Name")
    worker_tel_no = forms.CharField(max_length = 11,
                                    help_text = "Worker tel. no")
    worker_email = forms.CharField(max_length = 100,
                                   help_text = "Worker email address")
    cust_id = forms.ModelChoiceField(queryset = Customer.objects.all(),
                                     help_text = "Customer Company")
    
    class Meta:
        model = Worker
        fields = ('worker_name', 'worker_tel_no', 'worker_email', 'cust_id', )


class ProjectForm(forms.ModelForm):
    STATUS_CHOICES = [
        (0, 'Prep'),
        (1, 'Section'),
        (2, 'Image'),
        (3, 'Bill')
        ]
    
    
    cust_id = forms.ModelChoiceField(queryset = Customer.objects.all(),
                                     help_text = "Customer Company")
    project_date = forms.DateField(help_text = "Date",
                                   widget = forms.SelectDateWidget)
    status = forms.ChoiceField(choices = STATUS_CHOICES,
                               help_text = "Status")
    num_samples = forms.IntegerField(help_text = "Number of Samples",
                                     min_value = 0)
    specimen_procedure = forms.CharField(max_length = 500,
                                         help_text = "Specimen procedure")
    chemical_fixation = forms.CharField(max_length = 100,
                                        help_text = "Chemical fixation")
    neg_staining = forms.CharField(max_length = 100,
                                   help_text = "Negative Staining")
    cryofixation = forms.CharField(max_length = 100,
                                   help_text = "Cryofixation")
    tem_embedding_schedule = forms.CharField(max_length = 100,
                                             help_text = "TEM embedding schedule")
    dehydration = forms.CharField(max_length = 100,
                                  help_text = "Dehydration")
    resin = forms.CharField(max_length = 100,
                            help_text = "Resin")
    sem = forms.CharField(max_length = 3,
                          help_text = "SEM")
    sem_mount = forms.CharField(max_length = 50,
                                help_text = "SEM mount")
    fd = forms.CharField(max_length = 50,
                         help_text = "fd")
    cpd = forms.CharField(max_length = 50,
                          help_text = "cpd")
    sem_cost = forms.CharField(max_length = 50,
                          help_text = "sem cost")
    temp_time = forms.CharField(max_length = 50,
                                help_text = "temp time")
    immunolabelling = forms.CharField(max_length = 100,
                                      help_text = "Immunolabelling")
    first_dilution_time = forms.CharField(max_length = 100,
                                          help_text = "First dilution time")
    second_dilution_time = forms.CharField(max_length = 100,
                                           help_text = "Second dilution time")
    contrast_staining = forms.CharField(max_length = 100,
                                        help_text = "Contrast staining")
    comments_results = forms.CharField(max_length = 500,
                                       help_text = "Comments and results")
    
    class Meta:
        model = Project
        fields = ('cust_id', 'project_date', 'status', 'num_samples', 'specimen_procedure', 'chemical_fixation',
                  'neg_staining', 'cryofixation', 'tem_embedding_schedule',
                  'dehydration', 'resin', 'sem', 'sem_mount', 'fd', 'cpd',
                  'sem_cost', 'temp_time', 'immunolabelling', 'first_dilution_time',
                  'second_dilution_time', 'contrast_staining', 'comments_results', )


class WorkerProjectBridgeForm(forms.ModelForm):
    worker_id = forms.ModelChoiceField(queryset = Worker.objects.all(),
                                     help_text = "Choose Worker")
    project_id = forms.ModelChoiceField(queryset = Project.objects.all(),
                                     help_text = "Choose Project")
    
    class Meta:
        model = WorkerProjectBridge
        fields = ('worker_id', 'project_id', )


class BillForm(forms.ModelForm):
    billing_date = forms.DateField(widget = forms.SelectDateWidget,
                                   help_text = "Date")
    billing_address = forms.CharField(max_length = 100,
                                      help_text = "Billing Address")
    total_cost = forms.FloatField(help_text = "Total Cost",
                                  min_value = 0)
    cust_id = forms.ModelChoiceField(queryset = Customer.objects.all(),
                                     help_text = "Customer Company")
    
    class Meta:
        model = Bill
        fields = ('billing_date', 'billing_address', 'total_cost', 'cust_id')


class ProjectBillDetailsForm(forms.ModelForm):
    project_id = forms.ModelChoiceField(queryset = Project.objects.all(),
                                     help_text = "Choose Project")
    jeol1200tem_unit = forms.FloatField(help_text = "jeol1200tem unit",
                                        min_value = 0)
    jeol100sem_unit = forms.FloatField(help_text = "jeol100sem unit",
                                       min_value = 0)
    tem_processing_unit = forms.IntegerField(help_text = "TEM processing unit",
                                             min_value = 0)
    sectioning_stained_unit = forms.IntegerField(help_text = "Sectioning stained unit",
                                                 min_value = 0)
    sectioning_contrast_stained_unit = forms.IntegerField(help_text = "Sectioning contrast stained unit",
                                                          min_value = 0)
    negative_staining_unit = forms.IntegerField(help_text = "Negative staining unit",
                                                min_value = 0)
    sem_processing_mounting_unit = forms.IntegerField(help_text = "SEM processing mounting unit",
                                                      min_value = 0)
    sem_processing_fd_unit = forms.IntegerField(help_text = "SEM processing fd unit",
                                                min_value = 0)
    sem_unit = forms.IntegerField(help_text = "SEM unit",
                                  min_value = 0)
    immunolabelling_unit = forms.IntegerField(help_text = "Immunolabelling unit",
                                              min_value = 0)
    cryosectioning_unit = forms.IntegerField(help_text = "Cryosectioning unit",
                                             min_value = 0)
    freeze_fracture_unit = forms.IntegerField(help_text = "Freeze fracture unit",
                                              min_value = 0)
    ir_white_unit = forms.IntegerField(help_text = "ir white unit",
                                       min_value = 0)
    
    extra1_name = forms.CharField(max_length = 100,
                                  help_text = "First extra service name")
    extra1_cost = forms.FloatField(min_value = 0,
                                   help_text = "First extra service cost")
    extra2_name = forms.CharField(max_length = 100,
                                  help_text = "Second extra service name")
    extra2_cost = forms.FloatField(min_value = 0,
                                   help_text = "Second extra service cost")
    extra3_name = forms.CharField(max_length = 100,
                                  help_text = "Third extra service name")
    extra3_cost = forms.FloatField(min_value = 0,
                                   help_text = "Third extra service cost")
    
    total = forms.FloatField(min_value = 0,
                             help_text = "Total cost")
    
    class Meta:
        model = ProjectBillDetails
        fields = ('project_id', 'jeol1200tem_unit', 'jeol100sem_unit', 'tem_processing_unit',
                  'sectioning_stained_unit', 'sectioning_contrast_stained_unit',
                  'negative_staining_unit', 'sem_processing_mounting_unit', 
                  'sem_processing_fd_unit', 'sem_unit', 'immunolabelling_unit',
                  'cryosectioning_unit', 'freeze_fracture_unit', 'ir_white_unit',
                  'extra1_name', 'extra1_cost', 'extra2_name', 'extra2_cost',
                  'extra3_name', 'extra3_cost', 'total', )


class ProjectBillBridgeForm(forms.ModelForm):
    bill_id =  forms.ModelChoiceField(queryset = Bill.objects.all(),
                                     help_text = "Choose Bill")
    project_bill_id =  forms.ModelChoiceField(queryset = ProjectBillDetails.objects.all(),
                                     help_text = "Choose Project Bill")
    
    class Meta:
        model = ProjectBillBridge
        fields = ('bill_id', 'project_bill_id')
 





