from django.db import models
from django.utils import timezone


# Create your models here.
    
class Services(models.Model):
    service_id = models.AutoField(primary_key = True)
    cust_type = models.CharField(max_length = 100)
    discount = models.FloatField()
    jeol1200tem_cost = models.FloatField()
    jeol100sem_cost = models.FloatField()
    tem_processing_cost = models.FloatField()
    sectioning_stained_cost = models.FloatField()
    sectioning_contrast_stained_cost = models.FloatField()
    negative_staining_cost = models.FloatField()
    sem_processing_mounting_cost = models.FloatField()
    sem_processing_fd_cost = models.FloatField()
    sem_cost = models.FloatField()
    immunolabelling_cost = models.FloatField()
    cryosectioning_cost = models.FloatField()
    freeze_fracture_cost = models.FloatField()
    ir_white_cost = models.FloatField()
    
    def __str__(self):
        return str(self.service_id) + " - " + str(self.cust_type)
    
    class Meta:
        verbose_name_plural = 'Services'


class Customer(models.Model):
    cust_id = models.AutoField(primary_key = True)
    cust_name = models.CharField(max_length = 100)
    cust_tel_no = models.CharField(max_length = 11) #specify if numbers can be international
    cust_email = models.CharField(max_length = 100)
    cust_budget_code = models.IntegerField()
    service_id = models.ForeignKey(Services, on_delete=models.CASCADE, default=None)
    
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
    project_id = models.AutoField(primary_key = True)
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    project_date = models.DateField(default=timezone.now)
    num_samples = models.IntegerField()
    specimen_procedure = models.CharField(max_length = 500)
    chemical_fixation = models.CharField(max_length = 100)
    neg_staining = models.CharField(max_length = 100)
    cryofixation = models.CharField(max_length = 100)
    tem_embedding_schedule = models.CharField(max_length = 100)
    dehydration = models.CharField(max_length = 100)
    resin = models.CharField(max_length = 100)
    sem = models.CharField(max_length = 3)
    sem_mount = models.CharField(max_length = 50)
    fd = models.CharField(max_length = 50)
    cpd = models.CharField(max_length = 50)
    sem_cost = models.CharField(max_length = 50)
    temp_time = models.CharField(max_length = 50)
    immunolabelling = models.CharField(max_length = 100)
    first_dilution_time = models.CharField(max_length = 100)
    second_dilution_time = models.CharField(max_length = 100)
    contrast_staining = models.CharField(max_length = 100)
    comments_results = models.CharField(max_length = 500)
    
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
    billind_date = models.DateField(default=timezone.now)
    billing_address = models.CharField(max_length = 100)
    total_cost = models.IntegerField()
    cust_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    
    def __str__(self):
        return "Bill id: " + str(self.bill_id) + " for " + str(self.cust_id) + " : " + str(self.total_cost)
    
    
class ProjectBillDetails(models.Model):
    project_bill_id = models.AutoField(primary_key = True)
    project_id = models.ForeignKey(Project, on_delete=models.CASCADE, default=None)
    jeol1200tem_unit = models.IntegerField()
    jeol100sem_unit = models.IntegerField()
    tem_processing_unit = models.IntegerField()
    sectioning_stained_unit = models.IntegerField()
    sectioning_contrast_stained_unit = models.IntegerField()
    negative_staining_unit = models.IntegerField()
    sem_processing_mounting_unit = models.IntegerField()
    sem_processing_fd_unit = models.IntegerField()
    sem_unit = models.IntegerField()
    immunolabelling_unit = models.IntegerField()
    cryosectioning_unit = models.IntegerField()
    freeze_fracture_unit = models.IntegerField()
    ir_white_unit = models.IntegerField()
    
    extra1_name = models.CharField(max_length = 100)
    extra1_cost = models.FloatField()
    extra2_name = models.CharField(max_length = 100)
    extra2_cost = models.FloatField()
    extra3_name = models.CharField(max_length = 100)
    extra3_cost = models.FloatField()
    
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
        return str(self.bill_id) + " bolngs to " + str(self.project_bill_id)    
    
    
    
    
    
    
    
    
    