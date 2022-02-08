from django import forms
from imaging_system_app.models import Customer, Worker, Services, Bill, ProjectBillDetails, ProjectBillBridge, Project, WorkerProjectBridge
from django.utils import timezone
import datetime


class ServicesForm(forms.ModelForm):
    name = forms.CharField(max_length = 100,
                                help_text = "Name of Service")
    normal_price = forms.FloatField(help_text = "Price of Service")
    in_house_price = forms.FloatField(widget=forms.HiddenInput(), required = False)
    outside_price = forms.FloatField(widget=forms.HiddenInput(), required = False)
    
    class Meta:
        model = Services
        fields = ('name', 'normal_price', )


class CustomerForm(forms.ModelForm):
    DISCOUNT_CHOICES = [
        (0.5, 'In-House'),
        (1.0, 'Normal'),
        (1.5, 'Outside')
    ]

    cust_name = forms.CharField(max_length = 100,
                                help_text = "Customer Name")
    cust_tel_no = forms.CharField(max_length = 11,
                                  help_text = "Customer Tel. no")
    cust_email = forms.CharField(max_length = 100,
                                 help_text = "Customer email address")
    cust_budget_code = forms.IntegerField(help_text = "Budget code",
                                          min_value = 0)
    cust_type = forms.ChoiceField(choices = DISCOUNT_CHOICES,
                               help_text = "Discount")
    
    class Meta:
        model = Customer
        fields = ('cust_name', 'cust_tel_no', 'cust_email', 'cust_budget_code',
                  'cust_type', )


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
    
    project_date = forms.DateField(help_text = "Date",
                                   widget = forms.SelectDateWidget(years=range(2000, 2100)), initial=datetime.date.today)
    status = forms.ChoiceField(choices = STATUS_CHOICES,
                               help_text = "Status")
    num_samples = forms.IntegerField(help_text = "Number of Samples",
                                     min_value = 0)
    specimen_procedure = forms.CharField(max_length = 500,
                                         help_text = "Specimen procedure", required = False)
    chemical_fixation = forms.CharField(max_length = 100,
                                        help_text = "Chemical fixation", required = False)
    neg_staining = forms.CharField(max_length = 100,
                                   help_text = "Negative Staining", required = False)
    cryofixation = forms.CharField(max_length = 100,
                                   help_text = "Cryofixation", required = False)
    tem_embedding_schedule = forms.CharField(max_length = 100,
                                             help_text = "TEM embedding schedule", required = False)
    dehydration = forms.CharField(max_length = 100,
                                  help_text = "Dehydration", required = False)
    resin = forms.CharField(max_length = 100,
                            help_text = "Resin", required = False)
    sem = forms.CharField(max_length = 3,
                          help_text = "SEM", required = False)
    sem_mount = forms.CharField(max_length = 50,
                                help_text = "SEM mount", required = False)
    fd = forms.CharField(max_length = 50,
                         help_text = "fd", required = False)
    cpd = forms.CharField(max_length = 50,
                          help_text = "cpd", required = False)
    sem_cost = forms.CharField(max_length = 50,
                          help_text = "sem cost", required = False)
    temp_time = forms.CharField(max_length = 50,
                                help_text = "temp time", required = False)
    immunolabelling = forms.CharField(max_length = 100,
                                      help_text = "Immunolabelling", required = False)
    first_dilution_time = forms.CharField(max_length = 100,
                                          help_text = "First dilution time", required = False)
    second_dilution_time = forms.CharField(max_length = 100,
                                           help_text = "Second dilution time", required = False)
    contrast_staining = forms.CharField(max_length = 100,
                                        help_text = "Contrast staining", required = False)
    comments_results = forms.CharField(max_length = 500,
                                       help_text = "Comments and results", required = False)
    
    class Meta:
        model = Project
        fields = ('project_date', 'status', 'num_samples', 'specimen_procedure', 'chemical_fixation',
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
    billing_date = forms.DateField(widget = forms.SelectDateWidget(years=range(2000, 2100)),
                                   help_text = "Date", initial=datetime.date.today)
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
    jeol1200tem_unit = forms.FloatField(help_text = "jeol1200tem unit",
                                        min_value = 0, required = False)
    jeol100sem_unit = forms.FloatField(help_text = "jeol100sem unit",
                                       min_value = 0, required = False)
    tem_processing_unit = forms.IntegerField(help_text = "TEM processing unit",
                                             min_value = 0, required = False)
    sectioning_stained_unit = forms.IntegerField(help_text = "Sectioning stained unit",
                                                 min_value = 0, required = False)
    sectioning_contrast_stained_unit = forms.IntegerField(help_text = "Sectioning contrast stained unit",
                                                          min_value = 0, required = False)
    negative_staining_unit = forms.IntegerField(help_text = "Negative staining unit",
                                                min_value = 0, required = False)
    sem_processing_mounting_unit = forms.IntegerField(help_text = "SEM processing mounting unit",
                                                      min_value = 0, required = False)
    sem_processing_fd_unit = forms.IntegerField(help_text = "SEM processing fd unit",
                                                min_value = 0, required = False)
    sem_unit = forms.IntegerField(help_text = "SEM unit",
                                  min_value = 0, required = False)
    immunolabelling_unit = forms.IntegerField(help_text = "Immunolabelling unit",
                                              min_value = 0, required = False)
    cryosectioning_unit = forms.IntegerField(help_text = "Cryosectioning unit",
                                             min_value = 0, required = False)
    freeze_fracture_unit = forms.IntegerField(help_text = "Freeze fracture unit",
                                              min_value = 0, required = False)
    ir_white_unit = forms.IntegerField(help_text = "ir white unit",
                                       min_value = 0, required = False)
    
    extra1_name = forms.CharField(max_length = 100,
                                  help_text = "First extra service name", required = False)
    extra1_cost = forms.FloatField(min_value = 0,
                                   help_text = "First extra service cost", required = False)
    extra2_name = forms.CharField(max_length = 100,
                                  help_text = "Second extra service name", required = False)
    extra2_cost = forms.FloatField(min_value = 0,
                                   help_text = "Second extra service cost", required = False)
    extra3_name = forms.CharField(max_length = 100,
                                  help_text = "Third extra service name", required = False)
    extra3_cost = forms.FloatField(min_value = 0,
                                   help_text = "Third extra service cost", required = False)
    
    class Meta:
        model = ProjectBillDetails
        fields = ('jeol1200tem_unit', 'jeol100sem_unit', 'tem_processing_unit',
                  'sectioning_stained_unit', 'sectioning_contrast_stained_unit',
                  'negative_staining_unit', 'sem_processing_mounting_unit', 
                  'sem_processing_fd_unit', 'sem_unit', 'immunolabelling_unit',
                  'cryosectioning_unit', 'freeze_fracture_unit', 'ir_white_unit',
                  'extra1_name', 'extra1_cost', 'extra2_name', 'extra2_cost',
                  'extra3_name', 'extra3_cost', )


class ProjectBillBridgeForm(forms.ModelForm):
    bill_id =  forms.ModelChoiceField(queryset = Bill.objects.all(),
                                     help_text = "Choose Bill")
    project_bill_id =  forms.ModelChoiceField(queryset = ProjectBillDetails.objects.all(),
                                     help_text = "Choose Project Bill")
    
    class Meta:
        model = ProjectBillBridge
        fields = ('bill_id', 'project_bill_id')
 





