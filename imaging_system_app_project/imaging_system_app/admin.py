from django.contrib import admin

from .models import Customer, Worker

admin.site.register(Customer)
admin.site.register(Worker)
