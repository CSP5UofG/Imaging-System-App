from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User

from imaging_system_app.models import Services, Customer, Project


# ===================== MODELS TESTS =====================  #
class ServicesModelTests(TestCase):
    def test_can_create_service_objects(self):
        service = Services(name="test", normal_price=20, in_house_price=10,
                           outside_price=30, unit_name="hours")
        service.save()
        
        self.assertEqual(Services.objects.first(), service)

# ===================== VIEWS TESTS =====================  #
class IndexViewTests(TestCase):
    def test_index_with_no_projects_or_bills(self):
        create_superuser(self)
        response = self.client.get(reverse('imaging_system_app:index'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no recent projects.')
        self.assertQuerysetEqual(response.context['projects'], [])
        self.assertContains(response, 'There are no bills present.')
        self.assertQuerysetEqual(response.context['bills'], [])
    
    def test_index_with_one_project_only(self):
        create_superuser(self)
        add_project(1, 2)
        response = self.client.get(reverse('imaging_system_app:index'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEquals(len(response.context['projects']), 1)
        self.assertContains(response, 'There are no bills present.')
        self.assertQuerysetEqual(response.context['bills'], [])

            
class ServicesViewsTest(TestCase):
    def test_services_with_service(self):
        create_superuser(self)
        add_service("test", 20, "hours")
        add_service("test2", 20, "hours")
        response = self.client.get(reverse('imaging_system_app:services'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test")
        self.assertContains(response, "test2")
        self.assertEquals(len(response.context['services']), 2)
        
    def test_services_page_with_no_service(self):
        create_superuser(self)
        response = self.client.get(reverse('imaging_system_app:services'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no services present.')
        self.assertQuerysetEqual(response.context['services'], [])
    
    def test_add_services_contains_forms(self):
        create_superuser(self)
        response = self.client.get(reverse('imaging_system_app:add-service'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form")
    
    def test_edit_services_contains_correct_service(self):
        create_superuser(self)
        add_service("test", 20, "hours")
        response = self.client.get(reverse('imaging_system_app:edit-service', kwargs = {'id': 1}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form")
        self.assertContains(response, "test")
        self.assertContains(response, "20")
    
    def test_edit_services_nonexistent_service_redirects(self):
        create_superuser(self)
        response = self.client.get(reverse('imaging_system_app:edit-service', kwargs = {'id': 101}))
        
        self.assertEqual(response.status_code, 302)
    
    def test_add_services_post_correct(self):
        create_superuser(self)
        response = self.client.post(reverse('imaging_system_app:add-service'), data={"name": "test",
                                                                            "normal_price": 20,
                                                                            "unit_name": "hours"})
        test_service = Services.objects.get(name="test")
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_service.name, "test")
        self.assertEqual(test_service.normal_price, 20)
        self.assertEqual(test_service.in_house_price, 10)
        self.assertEqual(test_service.outside_price, 30)
    
    def test_edit_service_post_correct(self):
        create_superuser(self)
        add_service("test", 20, "hours")
        response = self.client.post(reverse('imaging_system_app:edit-service', kwargs = {'id': 1}),
                                    data={"name": "test2",
                                          "normal_price": 10,
                                          "unit_name": "sample"})
        test_service = Services.objects.get(name="test2")
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_service.name, "test2")
        self.assertEqual(test_service.normal_price, 10)
        self.assertEqual(test_service.in_house_price, 5)
        self.assertEqual(test_service.outside_price, 15)

class CustomerTests(TestCase):
    def test_all_customers_with_no_customer(self):
        create_superuser(self)
        response = self.client.get(reverse('imaging_system_app:customers'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no customers yet.')
        self.assertQuerysetEqual(response.context['customers'], [])
    
    def test_all_customers_with_customers(self):
        create_superuser(self)
        add_customer("test")
        add_customer("test2")
        response = self.client.get(reverse('imaging_system_app:customers'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test")
        self.assertContains(response, "test2")
        self.assertEquals(len(response.context['customers']), 2)
    
    def test_add_customers_contains_forms(self):
        create_superuser(self)
        response = self.client.get(reverse('imaging_system_app:add-customer'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form")
    
    def test_add_customers_post_correct(self):
        create_superuser(self)
        response = self.client.post(reverse('imaging_system_app:add-customer'),
                                    data={'cust_name': 'test',
                                          'cust_tel_no': '12345678910',
                                          'cust_email': 'email@email.com',
                                          'cust_budget_code': '101',
                                          'cust_type': '0.5'})
        test_customer = Customer.objects.get(cust_name = 'test')
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_customer.cust_name, "test")
        self.assertEqual(test_customer.cust_tel_no, "12345678910")
        self.assertEqual(test_customer.cust_email, "email@email.com")
        self.assertEqual(test_customer.cust_budget_code, 101)
        self.assertEqual(test_customer.cust_type, 0.5)
    
    def test_edit_customer_contains_correct_service(self):
        create_superuser(self)
        add_customer("test")
        response = self.client.get(reverse('imaging_system_app:edit-customer', kwargs = {'id': 1}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form")
        self.assertContains(response, "test")
        self.assertContains(response, "123456789101")
    
    def test_edit_customer_nonexistent_service_redirects(self):
        create_superuser(self)
        response = self.client.get(reverse('imaging_system_app:edit-customer', kwargs = {'id': 101}))
        
        self.assertEqual(response.status_code, 302)

    def test_edit_customer_post_correct(self):
        create_superuser(self)
        add_customer("test")
        response = self.client.post(reverse('imaging_system_app:edit-customer', kwargs = {'id': 1}),
                                    data={'cust_name': 'test-update',
                                          'cust_tel_no': '12345678912',
                                          'cust_email': 'email@email.com',
                                          'cust_budget_code': '103',
                                          'cust_type': '0.5'})
        test_customer = Customer.objects.get(cust_name="test-update")
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_customer.cust_name, "test-update")
        self.assertEqual(test_customer.cust_tel_no, "12345678912")
        self.assertEqual(test_customer.cust_email, "email@email.com")
        self.assertEqual(test_customer.cust_budget_code, 103)
        self.assertEqual(test_customer.cust_type, 0.5)
    
    def test_customer_details_page_contains_all_info(self):
        create_superuser(self)
        add_customer("test")
        response = self.client.get(reverse('imaging_system_app:customer-details', kwargs = {'id': 1}))
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(response.context['workers'], [])        
        self.assertQuerysetEqual(response.context['projects'], [])
        self.assertQuerysetEqual(response.context['bills'], [])
        self.assertContains(response, "test")
        self.assertContains(response, "123456789101")
        
        
class ProjectTests(TestCase):
    def test_all_projects_page_with_no_project(self):
        create_superuser(self)
        response = self.client.get(reverse('imaging_system_app:projects'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no projects present.')
        self.assertQuerysetEqual(response.context['projects'], [])
    
    def test_all_projects_page_with_projects(self):
        create_superuser(self)
        add_project(1, 2)
        add_project(1, 3)
        response = self.client.get(reverse('imaging_system_app:projects'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1")
        self.assertContains(response, "2")
        self.assertContains(response, "3")
        self.assertEquals(len(response.context['projects']), 2)
    
    def test_project_details_page_contains_correct_info(self):
        create_superuser(self)
        test_project = add_project(1, 2)
        response = self.client.get(reverse('imaging_system_app:project-details', kwargs = {'id': 1}))
        
        self.assertEqual(response.status_code, 200)
        self.assertQuerysetEqual(str(response.context['project']), "Project id: 1 Cost: 0.0") 
        self.assertEqual(response.context['project'], test_project) 
        self.assertQuerysetEqual(response.context['services'], [])
        self.assertQuerysetEqual(response.context['workers'], [])
        self.assertContains(response, "1")
        self.assertContains(response, "2")


class StatisticsTests(TestCase):
    def test_statistics_page_contains_correct_info(self):
        create_superuser(self)
        response = self.client.get(reverse('imaging_system_app:projects'))
        
        self.assertEqual(response.status_code, 200)
                
# ===================== HELPER FUNTCTIONS =====================  #
def add_service(name, price, unit_name):
    service = Services.objects.create(name=name,
                                      normal_price=price,
                                      in_house_price = price/2,
                                      outside_price = price*1.5,
                                      unit_name = unit_name)
    
    service.save()
    return service

def add_customer(cust_name):
    customer = Customer.objects.create(cust_name = cust_name,
                                       cust_tel_no = "123456789101",
                                       cust_email = "email@email.com",
                                       cust_budget_code = 101)
    customer.save()
    return customer
    
def create_superuser(self):
    self.user = User.objects.create_superuser(
        username='username', email='absoluetly@valid.com', password='top_secret')
    self.client.login(username='username', password='top_secret')
    return self

def add_project(status, num_samples):
    project = Project.objects.create(status = status,
                                     num_samples = num_samples)
    return project