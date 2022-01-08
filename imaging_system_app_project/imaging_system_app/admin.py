from django.contrib import admin

from .models import Customer, Worker, Services, Bill, ProjectBillDetails, ProjectBillBridge, Project, WorkerProjectBridge

admin.site.register(Customer)
admin.site.register(Worker)
admin.site.register(Services)
admin.site.register(Bill)
admin.site.register(ProjectBillDetails)
admin.site.register(ProjectBillBridge)
admin.site.register(Project)
admin.site.register(WorkerProjectBridge)
