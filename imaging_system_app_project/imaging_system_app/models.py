from django.db import models

# Create your models here.

class Customer(models.Model):
    cust_id = models.AutoField(primary_key = True)
    cust_name = models.CharField(max_length = 100)
    cust_tel_no = models.CharField(max_length = 11) #specify if numbers can be international
    cust_email = models.CharField(max_length = 100)
    cust_budget_code = models.IntegerField()
    #service_id = models.ForeignKey(Services, on_delete=models.CASCADE)
    
    def __str__(self):
        return str(self.cust_id) + " " + self.cust_name


class Worker(models.Model):
    worker_id = models.AutoField(primary_key = True)
    worker_name = models.CharField(max_length = 100)
    worker_tel_no = models.CharField(max_length = 11) #specify if numbers can be international
    worker_email = models.CharField(max_length = 100)
    cust_id = models.ForeignKey(Customer, on_delete = models.CASCADE)
    
    def __str__(self):
        return str(self.worker_id) + " " + self.worker_name + "works for: " + str(self.cust_id)
    
    