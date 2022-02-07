from django.urls import path
from imaging_system_app import views

app_name = 'imaging_system_app'

urlpatterns = [
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('projects/', views.projects, name='projects'),
    path('customers/', views.customers, name='customers'),
    path('customers/<cust_id>/', views.customerDetails, name='customerdetails'),
    path('customers/<cust_id>/edit', views.editCustomer, name='edit-customer'),
    path('workers/<worker_id>/edit', views.editWorker, name='edit-worker'),
    path('add-customer/', views.addCustomer, name='add-customer'),
    path('bills/', views.bills, name='bills'),
    path('add-service/', views.addService, name='add-service'),
    # sample view for queries
    path('queries/', views.queries, name='queries'),
]
