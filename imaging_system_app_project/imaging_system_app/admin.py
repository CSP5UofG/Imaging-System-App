from django.contrib import admin

from .models import Customer, Worker, Services, Bill, ProjectBillDetails, ProjectBillBridge, Project, WorkerProjectBridge

class ServicesAdmin(admin.ModelAdmin):
    list_display = ('cust_type', 'discount', )


admin.site.register(Services, ServicesAdmin)

class CustomerAdmin(admin.ModelAdmin):
    list_display = ('cust_id', 'cust_name', 'cust_tel_no', 'cust_email', 'cust_budget_code', 'get_cust_type', 'get_discount', )
    list_filter = ('service_id__cust_type', )
    search_fields = ('cust_name', 'cust_tel_no', 'cust_email', 'cust_budget_code', )
    def get_cust_type(self, obj): # Allows displaying customer type
        return obj.service_id.cust_type
    get_cust_type.admin_order_field  = 'service_id__cust_type'
    get_cust_type.short_description = 'Customer type'
    def get_discount(self, obj): # Allows displaying discount
        return obj.service_id.discount
    get_discount.admin_order_field  = 'service_id__discount'
    get_discount.short_description = 'Discount'

admin.site.register(Customer, CustomerAdmin)


class WorkerAdmin(admin.ModelAdmin):
    list_display = ('worker_id', 'worker_name', 'get_cust_id', 'get_cust_name', 'worker_tel_no', 'worker_email', )
    search_fields = ('cust_id__cust_name', 'worker_name', 'worker_email')
    def get_cust_id(self, obj): # Allows displaying customer id
        return obj.cust_id.cust_id
    get_cust_id.admin_order_field  = 'cust_id__cust_id'
    get_cust_id.short_description = 'Customer id'
    def get_cust_name(self, obj): # Allows displaying customer name 
        return obj.cust_id.cust_name
    get_cust_name.admin_order_field  = 'cust_id__cust_name'
    get_cust_name.short_description = 'Customer'

admin.site.register(Worker, WorkerAdmin)


class BillAdmin(admin.ModelAdmin):
    list_display = ('bill_id', 'billing_date', 'get_cust_id', 'get_cust_name', 'total_cost', )
    search_fields = ('cust_id__cust_name', )
    date_hierarchy = 'billing_date'
    def get_cust_id(self, obj): # Allows displaying customer id
        return obj.cust_id.cust_id
    get_cust_id.admin_order_field  = 'cust_id__cust_id'
    get_cust_id.short_description = 'Customer id'
    def get_cust_name(self, obj): # Allows displaying customer name 
        return obj.cust_id.cust_name
    get_cust_name.admin_order_field  = 'cust_id__cust_name'
    get_cust_name.short_description = 'Customer'

admin.site.register(Bill, BillAdmin)


class ProjectBillDetailsAdmin(admin.ModelAdmin):
    list_display = ('get_proj_id', 'get_proj_date', 'get_cust_id', 'get_cust_name', 'get_proj_samples', 'total', )
    search_fields = ('project_id__cust_id__cust_name', )
    date_hierarchy = 'project_id__project_date'
    def get_proj_id(self, obj): # Allows displaying project id
        return obj.project_id.project_id
    get_proj_id.admin_order_field  = 'project_id__project_id'
    get_proj_id.short_description = 'Project id'
    def get_proj_date(self, obj): # Allows displaying project date
        return obj.project_id.project_date
    get_proj_date.admin_order_field  = 'project_id__project_date'
    get_proj_date.short_description = 'Project date'
    def get_proj_samples(self, obj): # Allows displaying number of samples
        return obj.project_id.num_samples
    get_proj_samples.admin_order_field  = 'project_id__num_samples'
    get_proj_samples.short_description = 'Samples'
    def get_cust_id(self, obj): # Allows displaying customer id
        return obj.project_id.cust_id.cust_id
    get_cust_id.admin_order_field  = 'project_id__cust_id__cust_id'
    get_cust_id.short_description = 'Customer id'
    def get_cust_name(self, obj): # Allows displaying customer name
        return obj.project_id.cust_id.cust_name
    get_cust_name.admin_order_field  = 'project_id__cust_id__cust_name'
    get_cust_name.short_description = 'Customer'

admin.site.register(ProjectBillDetails, ProjectBillDetailsAdmin)


class ProjectBillBridgeAdmin(admin.ModelAdmin):
    list_display = ('get_billing_date', 'get_cust_id', 'get_cust_name', 'get_bill_id', 'get_bill_cost', 'get_proj_id', 'get_proj_cost')
    search_fields = ('bill_id__cust_id__cust_name', )
    date_hierarchy = 'bill_id__billing_date'    
    def get_billing_date(self, obj): # Allows displaying billing date
        return obj.bill_id.billing_date
    get_billing_date.admin_order_field  = 'bill_id__billing_date'
    get_billing_date.short_description = 'Billing date'
    def get_cust_id(self, obj): # Allows displaying customer id
        return obj.bill_id.cust_id.cust_id
    get_cust_id.admin_order_field  = 'bill_id__cust_id__cust_id'
    get_cust_id.short_description = 'Customer id'
    def get_cust_name(self, obj): # Allows displaying customer name
        return obj.bill_id.cust_id.cust_name
    get_cust_name.admin_order_field  = 'bill_id__cust_id__cust_name'
    get_cust_name.short_description = 'Customer'
    def get_bill_id(self, obj): # Allows displaying bill id
        return obj.bill_id.bill_id
    get_bill_id.admin_order_field  = 'bill_id__bill_id'
    get_bill_id.short_description = 'Bill id'
    def get_bill_cost(self, obj): # Allows displaying bill cost
        return obj.bill_id.total_cost
    get_bill_cost.admin_order_field  = 'bill_id__total_cost'
    get_bill_cost.short_description = 'Total cost'
    def get_proj_id(self, obj): # Allows displaying project id
        return obj.project_bill_id.project_id.project_id
    get_proj_id.admin_order_field  = 'project_bill_id__project_id__project_id'
    get_proj_id.short_description = 'Project id'
    def get_proj_cost(self, obj): # Allows displaying project cost
        return obj.project_bill_id.total
    get_proj_cost.admin_order_field  = 'project_bill_id__total'
    get_proj_cost.short_description = 'Project cost'
    
admin.site.register(ProjectBillBridge, ProjectBillBridgeAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'project_date', 'get_cust_id', 'get_cust_name', 'num_samples', )
    search_fields = ('cust_id__cust_name', )
    date_hierarchy = 'project_date'
    def get_cust_id(self, obj): # Allows displaying customer id
        return obj.cust_id.cust_id
    get_cust_id.admin_order_field  = 'cust_id__cust_id'
    get_cust_id.short_description = 'Customer id'
    def get_cust_name(self, obj): # Allows displaying customer name
        return obj.cust_id.cust_name
    get_cust_name.admin_order_field  = 'cust_id__cust_name'
    get_cust_name.short_description = 'Customer'

admin.site.register(Project, ProjectAdmin)

class WorkerProjectBridgeAdmin(admin.ModelAdmin):
    list_display = ('get_cust_id', 'get_cust_name', 'get_proj_id', 'get_proj_date', 'get_worker_id', 'get_worker_name', )
    search_fields = ('project_id__cust_id__cust_name', 'worker_id__worker_name', )
    date_hierarchy = 'project_id__project_date'
    def get_cust_id(self, obj): # Allows displaying customer id
        return obj.project_id.cust_id.cust_id
    get_cust_id.admin_order_field  = 'project_id__cust_id__cust_id'
    get_cust_id.short_description = 'Customer id'
    def get_cust_name(self, obj): # Allows displaying customer name
        return obj.project_id.cust_id.cust_name
    get_cust_name.admin_order_field  = 'project_id__cust_id__cust_name'
    get_cust_name.short_description = 'Customer name'
    def get_proj_id(self, obj): # Allows displaying project id
        return obj.project_id.project_id
    get_proj_id.admin_order_field  = 'project_id__project_id'
    get_proj_id.short_description = 'Project id'
    def get_proj_date(self, obj): # Allows displaying project date
        return obj.project_id.project_date
    get_proj_date.admin_order_field  = 'project_id__project_date'
    get_proj_date.short_description = 'Project date'
    def get_worker_id(self, obj): # Allows displaying worker id
        return obj.worker_id.worker_id
    get_worker_id.admin_order_field  = 'worker_id__worker_id'
    get_worker_id.short_description = 'Worker id'
    def get_worker_name(self, obj): # Allows displaying worker name
        return obj.worker_id.worker_name
    get_worker_name.admin_order_field  = 'worker_id__worker_name'
    get_worker_name.short_description = 'Worker'
    
admin.site.register(WorkerProjectBridge, WorkerProjectBridgeAdmin)

