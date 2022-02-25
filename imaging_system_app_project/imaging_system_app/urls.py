from django.urls import path
from imaging_system_app import views

app_name = 'imaging_system_app'

urlpatterns = [
    path('register/', views.register, name='register'), 
    path('login/', views.user_login, name='login'), 
    path('logout/', views.user_logout, name='logout'), 
    
    path('', views.index, name='index'),
    path('services/', views.services, name='services'),
    path('projects/', views.projects, name='projects'),
    path('customers/', views.customers, name='customers'),
    path('bills/', views.bills, name='bills'),
    
    path('add-service/', views.addService, name='add-service'),
    path('edit-service/<id>', views.editService, name='edit-service'),
    
    path('projects/<id>/', views.projectdetails, name='project-details'),
    path('add-project/', views.addProject, name='add-project'),
    path('projects/<id>/edit/', views.editProject, name='edit-project'),
    
    path('customers/<id>/', views.customerdetails, name='customer-details'),
    path('add-customer/', views.addCustomer, name='add-customer'),
    path('customers/<id>/edit/', views.editCustomer, name='edit-customer'),
    path('workers/<id>/edit/', views.editWorker, name='edit-worker'),
    
    path('bills/<id>/', views.billdetails, name='bill-details'),
    path('add-bill/', views.addBill, name='add-bill'),
    path('bills/<id>/edit/', views.editBill, name='edit-bill'),
    path('bills/<id>/print/', views.printBill, name='print-bill'),
    
    path('statistics/', views.viewStatistics, name='statistics'),
    path('ajax/getWorkers/', views.getWorkers, name='get-workers'),
]
