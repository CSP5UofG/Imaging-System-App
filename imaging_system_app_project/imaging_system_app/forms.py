from django import forms
from imaging_system_app.models import Customer, Worker, Services, Bill, ProjectServicesBridge, ProjectBillBridge, Project, WorkerProjectBridge
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import datetime


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = None
        self.fields['password'].help_text = "Letters, digits and special characters ( @ . + - _ ) only"
    
    class Meta:
        model = User
        fields = ('username', 'password')


class ServicesForm(forms.ModelForm):
    name = forms.CharField(max_length = 100,
                                help_text = "Name of Service")
    normal_price = forms.FloatField(help_text = "Price of Service")
    external_price = forms.FloatField(widget=forms.HiddenInput(), required = False)
    unit_name = forms.CharField(max_length = 20, help_text = "Unit name of Service")
    
    class Meta:
        model = Services
        fields = ('name', 'normal_price', 'unit_name')


class CustomerForm(forms.ModelForm):
    DISCOUNT_CHOICES = [
        (1.0, 'Normal'),
        (1.5, 'External')
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
    
    class Meta:
        model = Worker
        fields = ('worker_name', 'worker_tel_no', 'worker_email', )



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
                                         help_text = "Specimen/procedure", required = False)
    chemical_fixation = forms.CharField(max_length = 100,
                                        help_text = "Chemical Fixation", required = False)
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
                                help_text = "SEM Mount", required = False)
    fd = forms.CharField(max_length = 50,
                         help_text = "FD", required = False)
    cpd = forms.CharField(max_length = 50,
                          help_text = "CPD", required = False)
    sem_cost = forms.CharField(max_length = 50,
                          help_text = "SEM Cost", required = False)
    temp_time = forms.CharField(max_length = 50,
                                help_text = "Temp/Time", required = False)
    immunolabelling = forms.CharField(max_length = 100,
                                      help_text = "Immunolabelling", required = False)
    first_dilution_time = forms.CharField(max_length = 100,
                                          help_text = "1°Ab/dilution/time", required = False)
    second_dilution_time = forms.CharField(max_length = 100,
                                           help_text = "2°Ab-gold/dilution/time", required = False)
    contrast_staining = forms.CharField(max_length = 100,
                                        help_text = "Contrast staining", required = False)
    comments_results = forms.CharField(max_length = 500,
                                       help_text = "Comments/Results", required = False)
    
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
                                      help_text = "Billing Address", required = False)
    extra1_name = forms.CharField(max_length = 100,
                                  help_text = "First extra service name", required = False)
    extra1_cost = forms.FloatField(min_value = 0,
                                   help_text = "First extra service cost", required = False)
    extra2_name = forms.CharField(max_length = 100,
                                  help_text = "Second extra service name", required = False)
    extra2_cost = forms.FloatField(min_value = 0,
                                   help_text = "Second extra service cost", required = False)
    
    class Meta:
        model = Bill
        fields = ('billing_date', 'billing_address', 'extra1_name', 'extra1_cost',
                  'extra2_name', 'extra2_cost')


class ProjectServicesBridgeForm(forms.ModelForm):
    service_id = forms.ModelChoiceField(queryset = Services.objects.all(),
                                     help_text = "Service", initial=Services.__dict__)
    units = forms.FloatField(help_text = "Units", min_value = 0)
    
    def clean_units(self):
        form_data = self.cleaned_data
        if not form_data['units'].is_integer():
            if form_data['service_id'].unit_name != 'hour':
                raise ValidationError("Value must be an integer. ")
            elif not (form_data['units'] + .5).is_integer():
                raise ValidationError("Value must be in .5 increments. ")
        return float(form_data['units'])
    
    
    
    class Meta:
        model = ProjectServicesBridge
        fields = ('service_id', 'units', )

