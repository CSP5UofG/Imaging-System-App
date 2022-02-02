from django.db import models
from django.utils import timezone


# Create your models here.
    
class Services(models.Model):
    service_id = models.AutoField(primary_key = True)
    name = models.CharField(max_length = 100)
    price = models.FloatField()

    def __str__(self):
        return str(self.service_id) + " - " + str(self.name)
    
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
    cust_id = models.ForeignKey(Customer, on_delete = models.CASCADE)
    
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
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    project_date = models.DateField(default=timezone.now)
    num_samples = models.IntegerField()
    specimen_procedure = models.CharField(max_length = 500, blank=True)
    chemical_fixation = models.CharField(max_length = 100, blank=True)
    neg_staining = models.CharField(max_length = 100, blank=True)
    cryofixation = models.CharField(max_length = 100, blank=True)
    tem_embedding_schedule = models.CharField(max_length = 100, blank=True)
    dehydration = models.CharField(max_length = 100, blank=True)
    resin = models.CharField(max_length = 100, blank=True)
    sem = models.CharField(max_length = 3, blank=True)
    sem_mount = models.CharField(max_length = 50, blank=True)
    fd = models.CharField(max_length = 50, blank=True)
    cpd = models.CharField(max_length = 50, blank=True)
    sem_cost = models.CharField(max_length = 50, blank=True)
    temp_time = models.CharField(max_length = 50, blank=True)
    immunolabelling = models.CharField(max_length = 100, blank=True)
    first_dilution_time = models.CharField(max_length = 100, blank=True)
    second_dilution_time = models.CharField(max_length = 100, blank=True)
    contrast_staining = models.CharField(max_length = 100, blank=True)
    comments_results = models.CharField(max_length = 500, blank=True)
    status = models.IntegerField(choices = STATUS_CHOICES, default = 0) # prep section image bill
    
    
    def __str__(self):
        return str(self.project_id) + " ordered by: " + str(self.cust_id)
    
 
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
    total_cost = models.FloatField()
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    def __str__(self):
        return "Bill id: " + str(self.bill_id) + " for " + str(self.cust_id) + " : " + str(self.total_cost)
    
    
class ProjectBillDetails(models.Model):
    project_bill_id = models.AutoField(primary_key = True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, default=None)
    jeol1200tem_unit = models.FloatField(blank=True, null = True)
    jeol100sem_unit = models.FloatField(blank=True, null = True)
    tem_processing_unit = models.IntegerField(blank=True, null = True)
    sectioning_stained_unit = models.IntegerField(blank=True, null = True)
    sectioning_contrast_stained_unit = models.IntegerField(blank=True, null = True)
    negative_staining_unit = models.IntegerField(blank=True, null = True)
    sem_processing_mounting_unit = models.IntegerField(blank=True, null = True)
    sem_processing_fd_unit = models.IntegerField(blank=True, null = True)
    sem_unit = models.IntegerField(blank=True, null = True)
    immunolabelling_unit = models.IntegerField(blank=True, null = True)
    cryosectioning_unit = models.IntegerField(blank=True, null = True)
    freeze_fracture_unit = models.IntegerField(blank=True, null = True)
    ir_white_unit = models.IntegerField(blank=True, null = True)
    
    extra1_name = models.CharField(max_length = 100, blank=True)
    extra1_cost = models.FloatField(blank=True, null = True)
    extra2_name = models.CharField(max_length = 100, blank=True)
    extra2_cost = models.FloatField(blank=True, null = True)
    extra3_name = models.CharField(max_length = 100, blank=True)
    extra3_cost = models.FloatField(blank=True, null = True)
    
    total = models.FloatField()
    
    def __str__(self):
        return "Prjoect bill: " + str(self.project_bill_id) + " - " + str(self.total)
    
    class Meta:
        verbose_name_plural = 'Project bill details'

    
   
class ProjectBillBridge(models.Model):
    project_bill_bridge_id = models.AutoField(primary_key = True)
    bill_id = models.ForeignKey(Bill, on_delete=models.CASCADE)
    project_bill_id = models.ForeignKey(ProjectBillDetails, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.project_bill_id) + " is billed in " + str(self.bill_id)
    
    
    
    
    
    
    
    
    