from django.db import models
from django.utils import timezone


# Create your models here.
    
class Services(models.Model):
    service_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 100)
    normal_price = models.FloatField()
    in_house_price = models.FloatField()
    outside_price = models.FloatField()
    unit_name = models.CharField(max_length = 20)

    def __str__(self):
        return str(self.name)
    
    class Meta:
        verbose_name_plural = 'Services'


class Customer(models.Model):
    DISCOUNT_CHOICES = [
        (0.5, 'In-House'),
        (1.0, 'Normal'),
        (1.5, 'Outside')
    ]
        
    cust_id = models.AutoField(primary_key = True)
    cust_name = models.CharField(max_length = 100)
    cust_tel_no = models.CharField(max_length = 11) #specify if numbers can be international
    cust_email = models.CharField(max_length = 100)
    cust_budget_code = models.IntegerField()
    cust_type = models.FloatField(choices = DISCOUNT_CHOICES, default = 1)
    
    def __str__(self):
        return str(self.cust_id) + " " + str(self.cust_name)


class Worker(models.Model):
    worker_id = models.AutoField(primary_key = True)
    worker_name = models.CharField(max_length = 100)
    worker_tel_no = models.CharField(max_length = 11) #specify if numbers can be international
    worker_email = models.CharField(max_length = 100)
    cust_id = models.ForeignKey(Customer, on_delete = models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return str(self.worker_id) + " " + self.worker_name + " works for: " + str(self.cust_id)
    

class Project(models.Model):
    STATUS_CHOICES = [
        (0, 'Prep'),
        (1, 'Section'),
        (2, 'Image'),
        (3, 'Bill')
    ]
    project_id = models.AutoField(primary_key = True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    project_date = models.DateField(default=timezone.now)
    num_samples = models.IntegerField()
    specimen_procedure = models.CharField(max_length = 500, blank=True, verbose_name="Specimen/procedure")
    chemical_fixation = models.CharField(max_length = 100, blank=True, verbose_name="Chemical Fixation")
    neg_staining = models.CharField(max_length = 100, blank=True, verbose_name="Negative staining")
    cryofixation = models.CharField(max_length = 100, blank=True, verbose_name="Cryofixation")
    tem_embedding_schedule = models.CharField(max_length = 100, blank=True, verbose_name="TEM embedding schedule")
    dehydration = models.CharField(max_length = 100, blank=True, verbose_name="Dehydration")
    resin = models.CharField(max_length = 100, blank=True, verbose_name="Resin")
    sem = models.CharField(max_length = 3, blank=True, verbose_name="SEM")
    sem_mount = models.CharField(max_length = 50, blank=True, verbose_name="SEM Mount")
    fd = models.CharField(max_length = 50, blank=True, verbose_name="FD")
    cpd = models.CharField(max_length = 50, blank=True, verbose_name="CPD")
    sem_cost = models.CharField(max_length = 50, blank=True, verbose_name="SEM Cost")
    temp_time = models.CharField(max_length = 50, blank=True, verbose_name="Temp/Time")
    immunolabelling = models.CharField(max_length = 100, blank=True, verbose_name="Immunolabeling")
    first_dilution_time = models.CharField(max_length = 100, blank=True, verbose_name="1°Ab/dilution/time")
    second_dilution_time = models.CharField(max_length = 100, blank=True, verbose_name="2°Ab-gold/dilution/time")
    contrast_staining = models.CharField(max_length = 100, blank=True, verbose_name="Contrast staining")
    comments_results = models.CharField(max_length = 500, blank=True, verbose_name="Comments/Results")
    status = models.IntegerField(choices = STATUS_CHOICES, default = 0) # prep section image bill
    total = models.FloatField(default = 0)
    
    def get_fields(self):
        return [(field.verbose_name, field.value_to_string(self)) for field in self._meta.fields]
    
    def __str__(self):
        return "Project id: " + str(self.project_id) + " Cost: " + str(self.total)
    
 
class WorkerProjectBridge(models.Model):
    worker_project_bridge_id = models.AutoField(primary_key = True)
    worker_id = models.ForeignKey(Worker, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    def __str__(self):
        return "Project id: " + str(self.project_id) + " Worker: " + str(self.worker_id) 
  
    
class Bill(models.Model):
    bill_id = models.AutoField(primary_key = True)
    billing_date = models.DateField(default=timezone.now)
    billing_address = models.CharField(max_length = 100, blank=True)
    extra1_name = models.CharField(max_length = 100, blank=True)
    extra1_cost = models.FloatField(blank=True, null = True)
    extra2_name = models.CharField(max_length = 100, blank=True)
    extra2_cost = models.FloatField(blank=True, null = True)
    total_cost = models.FloatField()
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    def __str__(self):
        return "Bill id: " + str(self.bill_id) + " for " + str(self.cust_id) + " : " + str(self.total_cost)
    
    
class ProjectServicesBridge(models.Model):
    project_services_bridge_id = models.AutoField(primary_key = True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, null=True, blank=True)
    service_id = models.ForeignKey(Services, on_delete=models.CASCADE)
    units = models.FloatField()
    cost = models.FloatField(default=0)
    
    def __str__(self):
        return str(self.project_id) + " - " + str(self.units) + "x " + str(self.service_id.name) + " Cost: " + str(self.cost)
    
   
class ProjectBillBridge(models.Model):
    project_bill_bridge_id = models.AutoField(primary_key = True)
    bill_id = models.ForeignKey(Bill, on_delete=models.CASCADE)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.project_id) + " is billed in " + str(self.bill_id)
    
    
    
    
    
    
    
    
    