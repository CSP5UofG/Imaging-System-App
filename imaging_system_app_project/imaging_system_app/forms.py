from django import forms
from imaging_system_app.models import Customer, Worker, Services, Bill, ProjectBillDetails, ProjectBillBridge, Project, WorkerProjectBridge
from django.utils import timezone


class ServicesForm(forms.ModelForm):
    cust_type = forms.CharField(max_length = 100)
    discount = forms.FloatField(help_text = "Discount")
    jeol1200tem_cost = forms.FloatField(help_text = "jeol1200tem cost")
    jeol100sem_cost = forms.FloatField(help_text = "jeol100sem cost")
    tem_processing_cost = forms.FloatField(help_text = "tem processing cost")
    sectioning_stained_cost = forms.FloatField(help_text = "sectioning stained cost")
    sectioning_contrast_stained_cost = forms.FloatField(help_text = "sectioning contrast stained cost")
    negative_staining_cost = forms.FloatField(help_text = "negative staining cost")
    sem_processing_mounting_cost = forms.FloatField(help_text = "sem processing mounting cost")
    sem_processing_fd_cost = forms.FloatField(help_text = "sem processing fd cost")
    sem_cost = forms.FloatField(help_text = "sem cost")
    immunolabelling_cost = forms.FloatField(help_text = "immunolabelling cost")
    cryosectioning_cost = forms.FloatField(help_text = "cryosectioning cost")
    freeze_fracture_cost = forms.FloatField(help_text = "freeze fracture cost")
    ir_white_cost = forms.FloatField(help_text = "ir white cost")
    
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
    cust_budget_code = forms.IntegerField(help_text = "Budget code")
    service_id = forms.ModelChoiceField(queryset = Services.objects.all(),
                                        help_text = "Choose Customer Type")
    
    class Meta:
        model = Customer
        fields = ('cust_name', 'cust_tel_no', 'cust_email', 'cust_budget_code',
                  'service_id', )
