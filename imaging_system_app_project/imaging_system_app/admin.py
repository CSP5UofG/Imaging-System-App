from django.contrib import admin
from django.contrib.auth.models import User

from .models import Customer, Worker, Services, Bill, ProjectServicesBridge, ProjectBillBridge, Project, WorkerProjectBridge


@admin.action(description='Activate user')
def activate_user(modeladmin, request, queryset):
    queryset.update(is_active=True)
    
@admin.action(description='Disable user')
def disable_user(modeladmin, request, queryset):
    queryset.update(is_active=False)
    
@admin.action(description='Give staff previleges to use the admin site')
def allocate_staff(modeladmin, request, queryset):
    queryset.update(is_staff=True)
    
@admin.action(description='Revoke staff previleges to use the admin site')
def revoke_staff(modeladmin, request, queryset):
    queryset.update(is_staff=False)

class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'is_active', 'is_staff', 'date_joined')
    ordering = ('-date_joined',)
    actions = [activate_user, disable_user, allocate_staff, revoke_staff]
    # add actions to User dropdown list

admin.site.unregister(User) # Overwrite built-in user admin
admin.site.register(User, UserAdmin)


class ServicesAdmin(admin.ModelAdmin):
    list_display = ('name', 'normal_price', 'external_price', 'unit_name')

admin.site.register(Services, ServicesAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ('cust_id', 'cust_name', 'cust_tel_no', 'cust_email', 'cust_budget_code', 'cust_type')
    search_fields = ('cust_name', 'cust_tel_no', 'cust_email', 'cust_budget_code', )

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


class ProjectServicesBridgeAdmin(admin.ModelAdmin):
    list_display = ('get_project_id', 'get_cust_name', 'get_project_total', 'get_service_name', 'units', 'cost')
    search_fields = ('project_id__cust_id__cust_name', )
    date_hierarchy = 'project_id__project_date'
    def get_project_id(self, obj): # Allows displaying project id
        return obj.project_id.project_id
    get_project_id.admin_order_field  = 'project_id__project_id'
    get_project_id.short_description = 'Project id'
    def get_cust_name(self, obj): # Allows displaying customer name
        return obj.project_id.cust_id.cust_name
    get_cust_name.admin_order_field  = 'project_id__cust_id__cust_name'
    get_cust_name.short_description = 'Customer'
    def get_project_total(self, obj): # Allows displaying project total
        return obj.project_id.total
    get_project_total.admin_order_field  = 'project_id__total'
    get_project_total.short_description = 'Project cost'
    def get_service_name(self, obj): # Allows displaying service name
        return obj.service_id.name
    get_service_name.admin_order_field  = 'service_id__name'
    get_service_name.short_description = 'Service name'

admin.site.register(ProjectServicesBridge, ProjectServicesBridgeAdmin)


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
    get_bill_cost.short_description = 'Bill cost'
    def get_proj_id(self, obj): # Allows displaying project id
        return obj.project_id.project_id
    get_proj_id.admin_order_field  = 'project_id__project_id'
    get_proj_id.short_description = 'Project id'
    def get_proj_cost(self, obj): # Allows displaying project cost
        return obj.project_id.total
    get_proj_cost.admin_order_field  = 'project_id__total'
    get_proj_cost.short_description = 'Project cost'
    
admin.site.register(ProjectBillBridge, ProjectBillBridgeAdmin)


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('project_id', 'project_date', 'get_cust_id', 'get_cust_name', 'num_samples', 'status', 'total')
    list_filter = ('status', )
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

