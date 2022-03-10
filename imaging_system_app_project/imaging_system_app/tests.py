from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone

from imaging_system_app.models import Services, Customer, Project, Worker, WorkerProjectBridge, ProjectServicesBridge, ProjectBillBridge, Bill


# ===================== MODELS TESTS =====================  #
class ServicesModelTests(TestCase):
    def test_can_create_service_objects(self):
        service = Services(name="test", normal_price=20, 
                           external_price=30, unit_name="hours")
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
        self.assertEqual(test_service.external_price, 30)
    
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
        self.assertEqual(test_service.external_price, 15)

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
                                          'cust_type': '1.0'})
        test_customer = Customer.objects.get(cust_name = 'test')
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_customer.cust_name, "test")
        self.assertEqual(test_customer.cust_tel_no, "12345678910")
        self.assertEqual(test_customer.cust_email, "email@email.com")
        self.assertEqual(test_customer.cust_budget_code, 101)
        self.assertEqual(test_customer.cust_type, 1.0)
    
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
                                          'cust_type': '1.0'})
        test_customer = Customer.objects.get(cust_name="test-update")
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_customer.cust_name, "test-update")
        self.assertEqual(test_customer.cust_tel_no, "12345678912")
        self.assertEqual(test_customer.cust_email, "email@email.com")
        self.assertEqual(test_customer.cust_budget_code, 103)
        self.assertEqual(test_customer.cust_type, 1.0)
    
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
    
    def test_add_project_contains_correct_info(self):
        create_superuser(self)
        test_customer = add_customer("test")
        test_worker = add_worker("bobTEST", test_customer)
        response = self.client.get(reverse('imaging_system_app:add-project'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['all_customer']), 1)
        self.assertContains(response, "TEM embedding schedule")
        self.assertContains(response, "Units")
        self.assertContains(response, "Service")
    
    def test_add_project_post_correct(self):
        create_superuser(self)
        test_customer = add_customer("test")
        test_worker = add_worker("bobTEST", test_customer)
        other_test_worker = add_worker("TESTbob", test_customer)
        test_service = add_service("test", 20, 'hours')
        other_test_service = add_service("other_test", 35, "hours")
        response = self.client.post(reverse('imaging_system_app:add-project'),
                                    data={'customer_id': 1,
                                          'worker_id': ['1', '2'],
                                          'project_date_month': 2,
                                          'project_date_day': 26,
                                          'project_date_year': 2022,
                                          'status': 1,
                                          'num_samples': 1,
                                          'specimen_procedure': '',
                                          'chemical_fixation': '',
                                          'neg_staining': '',
                                          'cryofixation': '',
                                          'tem_embedding_schedule': '',
                                          'dehydration': '',
                                          'resin': '',
                                          'sem': '',
                                          'sem_mount': '',
                                          'fd': '',
                                          'cpd': '',
                                          'sem_cost': '',
                                          'temp_time': '',
                                          'immunolabelling': '',
                                          'first_dilution_time': '',
                                          'second_dilution_time': '',
                                          'contrast_staining': '',
                                          'comments_results': '',
                                          'service_id': '1',
                                          'units': '1',
                                          'form-TOTAL_FORMS': 2,
                                          'form-INITIAL_FORMS': 0,
                                          'form-MIN_NUM_FORMS': 0,
                                          'form-MAX_NUM_FORMS': 1000,
                                          'form-0-service_id': 1,
                                          'form-0-units': 1,
                                          'form-1-service_id': 2,
                                          'form-1-units': 1, })
        test_project = Project.objects.get(project_id = 1)
        test_WPBridge = WorkerProjectBridge.objects.filter(project_id = 1)
        test_PSBridge = ProjectServicesBridge.objects.filter(service_id = 1)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_project.status, 1)
        self.assertEqual(len(test_WPBridge), 2)
        self.assertEqual(len(test_WPBridge), 2)
        self.assertEqual(test_project.cust_id, test_customer)
        self.assertEqual(test_PSBridge[0].project_id, test_project)
        self.assertEqual(test_project.total, 55)
    
    def test_edit_project_contains_correct_info(self):
        create_superuser(self)
        test_customer = add_customer("test")
        test_worker = add_worker("bobTEST", test_customer)
        test_project = add_project(1, 25)
        test_service = add_service("test", 20, 'hours')
        test_project.cust_id = test_customer
        test_project.save()
        WorkerProjectBridge.objects.create(worker_id=test_worker, project_id=test_project)
        ProjectServicesBridge.objects.create(project_id=test_project, service_id=test_service,
                                             units = 2, cost = 20)
        response = self.client.get(reverse('imaging_system_app:edit-project', kwargs = {'id': 1}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "TEM embedding schedule")
        self.assertContains(response, "Units")
        self.assertContains(response, "Service")
        self.assertContains(response, "bobTEST")
        self.assertContains(response, "25")
        
    def test_edit_project_post_correct(self):
        create_superuser(self)
        test_customer = add_customer("test")
        other_customer = add_customer("test2")
        test_worker = add_worker("bobTEST", test_customer)
        other_worker = add_worker("TESTbob", other_customer)
        test_service = add_service("test", 20, 'hours')
        test_project = add_project(1, 25)
        test_bill = add_bill(test_customer)
        test_project.cust_id = test_customer
        test_project.save()
        WorkerProjectBridge.objects.create(worker_id=test_worker, project_id=test_project)
        ProjectServicesBridge.objects.create(project_id=test_project, service_id=test_service,
                                             units = 2, cost = 20)
        ProjectBillBridge.objects.create(project_id = test_project,
                                                                  bill_id = test_bill)

        response = self.client.post(reverse('imaging_system_app:edit-project', kwargs = {'id': test_project.project_id}),
                                    data={'customer_id': [other_customer.cust_id],
                                          'worker_id': other_worker.worker_id,
                                          'project_date_month': ['8'],
                                          'project_date_day': ['11'],
                                          'project_date_year': ['2021'],
                                          'status': ['0'],
                                          'num_samples': ['3'],
                                          'specimen_procedure': [''],
                                          'chemical_fixation': [''],
                                          'neg_staining': [''],
                                          'cryofixation': [''],
                                          'tem_embedding_schedule': [''],
                                          'dehydration': [''],
                                          'resin': [''],
                                          'sem': [''],
                                          'sem_mount': [''],
                                          'fd': [''],
                                          'cpd': [''],
                                          'sem_cost': [''],
                                          'temp_time': [''],
                                          'immunolabelling': [''],
                                          'first_dilution_time': [''],
                                          'second_dilution_time': [''],
                                          'contrast_staining': [''],
                                          'comments_results': [''],
                                          'service_id': ['1'],
                                          'units': ['1.0'],})
        
        check_project = Project.objects.get(project_id = 1)
        test_WPBridge = WorkerProjectBridge.objects.get(project_id = 1)
        test_PSBridge = ProjectServicesBridge.objects.get(service_id = 1)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(check_project.status, 0)
        self.assertEqual(test_WPBridge.worker_id.worker_name, "TESTbob")
        self.assertEqual(test_WPBridge.project_id, test_project)
        self.assertEqual(check_project.cust_id, other_customer)
        self.assertEqual(test_PSBridge.project_id, test_project)
    
    def test_edit_nonexistent_project_redirects(self):
        create_superuser(self)
        test_customer = add_customer("test")
        test_worker = add_worker("bobTEST", test_customer)
        test_project = add_project(1, 25)
        test_service = add_service("test", 20, 'hours')
        test_project.cust_id = test_customer
        WorkerProjectBridge.objects.create(worker_id=test_worker, project_id=test_project)
        ProjectServicesBridge.objects.create(project_id=test_project, service_id=test_service,
                                             units = 2, cost = 20)
        response = self.client.get(reverse('imaging_system_app:edit-project', kwargs = {'id': 102}))
        
        self.assertEqual(response.status_code, 302)
    


class StatisticsTests(TestCase):
    def test_statistics_page_contains_correct_info(self):
        create_superuser(self)
        response = self.client.get(reverse('imaging_system_app:projects'))
        
        self.assertEqual(response.status_code, 200)

class WorkerTests(TestCase):
    def test_customer_details_with_worker(self):
        create_superuser(self)
        test_customer = add_customer("test")
        test_worker = add_worker("bobTEST", test_customer)
        response = self.client.get(reverse('imaging_system_app:customer-details', kwargs = {'id': 1}))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['workers']), 1)        
        self.assertContains(response, "bobTEST")
    
    def test_add_worker_contain_correct_info(self):
        create_superuser(self)
        test_customer = add_customer("test")
        response = self.client.get(reverse('imaging_system_app:add-worker', kwargs = {'id': 1}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "worker_form")
    
    def test_add_worker_correct_post(self):
        create_superuser(self)
        add_customer("test")
        response = self.client.post(reverse('imaging_system_app:add-worker', kwargs = {'id': 1}),
                                    data={'worker_name': 'TESTbob',
                                          'worker_tel_no': '12345678912',
                                          'worker_email': 'email@email.com',})
        test_worker = Worker.objects.get(worker_name="TESTbob")
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_worker.worker_name, "TESTbob")
        self.assertEqual(test_worker.worker_tel_no, "12345678912")
        self.assertEqual(test_worker.worker_email, "email@email.com")
    
    def test_edit_worker_contain_correct_info(self):
        create_superuser(self)
        test_customer = add_customer("test")
        test_worker = add_worker("bobTEST", test_customer)
        response = self.client.get(reverse('imaging_system_app:edit-worker', kwargs = {'id': 1}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form")
    
    def test_edit_worker_correct_post(self):
        create_superuser(self)
        test_customer = add_customer("test")
        test_worker = add_worker("bobTEST", test_customer)
        response = self.client.post(reverse('imaging_system_app:edit-worker', kwargs = {'id': 1}),
                                    data={'worker_name': 'TESTbobTEST',
                                          'worker_tel_no': '12345678912',
                                          'worker_email': 'email@email.com',})
        test_worker = Worker.objects.get(worker_name="TESTbobTEST")
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_worker.worker_name, "TESTbobTEST")
        self.assertEqual(test_worker.worker_tel_no, "12345678912")
        self.assertEqual(test_worker.worker_email, "email@email.com")
    
    def test_edit_worker_nonexistent_service_redirects(self):
        create_superuser(self)
        response = self.client.get(reverse('imaging_system_app:edit-worker', kwargs = {'id': 101}))
        
        self.assertEqual(response.status_code, 302)


class BillingTests(TestCase):
    def test_all_bills_page_with_no_bills(self):
        create_superuser(self)
        response = self.client.get(reverse('imaging_system_app:bills'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'There are no bills present.')
        self.assertQuerysetEqual(response.context['bills'], [])
    
    def test_all_bills_page_with_bills(self):
        create_superuser(self)
        test_customer = add_customer("test_customer")
        first_test_bill = add_bill(test_customer)
        second_test_bill = add_bill(test_customer)
        response = self.client.get(reverse('imaging_system_app:bills'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "1")
        self.assertContains(response, "test_customer")
        self.assertEquals(len(response.context['bills']), 2)
    
    def test_bill_details_page_contains_correct_info(self):
        create_superuser(self)
        test_customer = add_customer("test_customer")
        first_test_bill = add_bill(test_customer)
        test_project = add_project(1, 2)
        test_project.cust_id = test_customer
        test_project.save()
        ProjectBillBridge.objects.create(bill_id = first_test_bill,
                                 project_id = test_project)
        response = self.client.get(reverse('imaging_system_app:bill-details', kwargs = {'id': 1}))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['bill'], first_test_bill) 
        self.assertContains(response, "test_customer")
        self.assertContains(response, "Fake Street 6")
    
    def test_add_bill_contains_correct_info(self):
        create_superuser(self)
        add_customer("test")
        add_customer("test2")
        response = self.client.get(reverse('imaging_system_app:add-bill'))
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['customers']), 2)
        self.assertContains(response, "Second extra service")
        self.assertContains(response, "Select a project")
        self.assertContains(response, "Select a customer")
    
    def test_add_bill_post_correct(self):
        create_superuser(self)
        test_customer = add_customer("test")
        test_project = add_project(1, 2)
        test_project.cust_id = test_customer
        test_project.save()
        response = self.client.post(reverse('imaging_system_app:add-bill'),
                                    data={'customer_id': '1',
                                          'project_id': '1',
                                          'billing_date_month': '3',
                                          'billing_date_day': '2',
                                          'billing_date_year': '2022',
                                          'billing_address': 'Fake street 5',
                                          'extra1_name': '',
                                          'extra1_cost': '',
                                          'extra2_name': '',
                                          'extra2_cost': '',})
        test_bill = Bill.objects.get(bill_id = 1)
        test_BPBridge = ProjectBillBridge.objects.get(bill_id = 1)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_bill.billing_address, 'Fake street 5')
        self.assertEqual(test_BPBridge.bill_id, test_bill)
        self.assertEqual(test_BPBridge.project_id, test_project)
    
    def test_edit_bill_contains_correct_info(self):
        create_superuser(self)
        test_customer = add_customer("test_customer")
        first_test_bill = add_bill(test_customer)
        test_project = add_project(1, 2)
        test_project.cust_id = test_customer
        test_project.save()
        ProjectBillBridge.objects.create(bill_id = first_test_bill,
                                 project_id = test_project)
        response = self.client.get(reverse('imaging_system_app:edit-bill', kwargs = {'id': 1}))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Second extra service name")
        self.assertContains(response, "First extra service cost")
        
    def test_edit_bill_post_correct(self):
        create_superuser(self)
        test_customer = add_customer("test_customer")
        first_test_bill = add_bill(test_customer)
        test_worker = add_worker("bob", test_customer)
        test_project = add_project(1, 2)
        test_project.cust_id = test_customer
        test_project.save()
        ProjectBillBridge.objects.create(bill_id = first_test_bill,
                                 project_id = test_project)
        WorkerProjectBridge.objects.create(worker_id=test_worker, project_id=test_project)

        response = self.client.post(reverse('imaging_system_app:edit-bill', kwargs = {'id': 1}),
                                    data={'billing_date_month': '3',
                                          'billing_date_day': '2',
                                          'billing_date_year': '2022',
                                          'billing_address': 'Fake street 5',
                                          'extra1_name': 'Extra fee',
                                          'extra1_cost': '200',
                                          'extra2_name': '',
                                          'extra2_cost': ''})
        
        test_bill = Bill.objects.get(bill_id = 1)
        test_BPBridge = ProjectBillBridge.objects.get(bill_id = 1)
        
        self.assertEqual(response.status_code, 302)
        self.assertEqual(test_bill.billing_address, 'Fake street 5')
        self.assertEqual(test_BPBridge.bill_id, test_bill)
        self.assertEqual(test_BPBridge.project_id, test_project)
        self.assertEqual(test_bill.extra1_name, 'Extra fee')
        self.assertEqual(test_bill.extra1_cost, 200)
           
    def test_edit_nonexistent_bill_redirects(self):
        create_superuser(self)
        test_customer = add_customer("test_customer")
        first_test_bill = add_bill(test_customer)
        test_worker = add_worker("bob", test_customer)
        test_project = add_project(1, 2)
        test_project.cust_id = test_customer
        test_project.save()
        ProjectBillBridge.objects.create(bill_id = first_test_bill,
                                 project_id = test_project)
        WorkerProjectBridge.objects.create(worker_id=test_worker, project_id=test_project)

        response = self.client.get(reverse('imaging_system_app:edit-bill', kwargs = {'id': 102}))
        
        self.assertEqual(response.status_code, 302)


class UserAuthTests(TestCase):
    def test_site_redirects_to_login_if_not_logged_in(self):
        response = self.client.get(reverse('imaging_system_app:index'))
        self.assertEqual(response.status_code, 302)
    
    def test_login_page_contains_correct_info(self):
        response = self.client.get(reverse('imaging_system_app:login'))
        self.assertContains(response, "Username:")
        self.assertContains(response, "Password:")
    
    def test_login_page_post_correct(self):
        create_superuser(self)
        response = self.client.post(reverse('imaging_system_app:login'),
                                            data = {'username': 'username',
                                                    'password': 'top_secret'})
        self.assertEqual(response.status_code, 302)
    
    def test_wrong_login_detected(self):
        create_superuser(self)
        response = self.client.post(reverse('imaging_system_app:login'),
                                            data = {'username': 'wrong_username',
                                                    'password': 'not_top_secret'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You have either entered invalid login details or your account has not been activated yet.")
    
    def test_registration_page_contains_correct_info(self):
        response = self.client.get(reverse('imaging_system_app:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Goto Login')
        self.assertContains(response, 'Register')
        self.assertContains(response, 'Username')
        self.assertContains(response, 'Password')
        self.assertContains(response, 'user_form')
    
    def test_registration_page_post_correct(self):
        response = self.client.post(reverse('imaging_system_app:register'),
                                            data = {'username': 'new_username',
                                                    'password': 'another_top_secret'})
        user = User.objects.get(username = 'new_username')
        
        self.assertEqual(response.status_code, 200)
        self.assertFalse(user.is_active)
        self.assertContains(response, 'Thank you for registering, note that admin approval is needed for account activation.')
    
    def test_logout_view_redirects_login_page(self):
        create_superuser(self)
        response = self.client.get(reverse('imaging_system_app:logout'))
        self.assertRedirects(response, '/imaging_system_app/login/')       


class QueryTests(TestCase):
    def test_service_queries(self):
        create_superuser(self)
        add_service("test", 20, "hours")
        add_service("something_else", 20, "hours")
        response = self.client.post(reverse('imaging_system_app:services'),
                                            data={'service_name': 'test'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test")
        self.assertEquals(len(response.context['services']), 1)

    def test_service_queries_non_existent(self):
        create_superuser(self)
        add_service("test", 20, "hours")
        add_service("something_else", 20, "hours")
        response = self.client.post(reverse('imaging_system_app:services'),
                                            data={'service_name': 'non-existent-service'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no services present.")
        self.assertEquals(len(response.context['services']), 0)

    def test_customer_queries(self):
        create_superuser(self)
        add_customer("test")
        add_customer("test2")
        response = self.client.post(reverse('imaging_system_app:customers'),
                                            data={'customer_query': 'test2'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "test2")
        self.assertEquals(len(response.context['customers']), 1)
    
    def test_customer_queries_non_existent(self):
        create_superuser(self)
        add_customer("test")
        add_customer("test2")
        response = self.client.post(reverse('imaging_system_app:customers'),
                                            data={'customer_query': 'invalid_customer'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no customers yet.")
        self.assertEquals(len(response.context['customers']), 0)
    
    def test_project_queries(self):
        create_superuser(self)
        test_project = add_project(1, 2)
        other_test_project = add_project(1, 3)
        test_customer = add_customer("test")
        other_test_customer = add_customer("test2")
        test_project.cust_id = test_customer
        test_project.project_date = '2000-01-01'
        test_project.save()
        other_test_project.cust_id = other_test_customer
        other_test_project.project_date = '2022-11-11'
        other_test_project.save()

        response = self.client.post(reverse('imaging_system_app:projects'),
                                            data={'project_customer': 'test2',
                                                  'project_from': '2022-01-02',
                                                  'project_to': '2022-12-12'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2")
        self.assertEquals(len(response.context['projects']), 1)

    def test_project_queries_non_existent(self):
        create_superuser(self)
        test_project = add_project(1, 2)
        other_test_project = add_project(1, 3)
        test_customer = add_customer("test")
        other_test_customer = add_customer("test2")
        test_project.cust_id = test_customer
        test_project.save()
        other_test_project.cust_id = other_test_customer
        other_test_project.save()

        response = self.client.post(reverse('imaging_system_app:projects'),
                                            data={'project_customer': 'invalid_project'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no projects present.")
        self.assertEquals(len(response.context['projects']), 0)

    
    def test_bill_queries(self):
        create_superuser(self)
        test_customer = add_customer("test_customer")
        other_test_customer = add_customer("test2")
        first_test_bill = add_bill(test_customer)
        first_test_bill.billing_date = '2022-01-01'
        first_test_bill.save()
        second_test_bill = add_bill(other_test_customer)
        second_test_bill.billing_date = '2022-11-11'
        second_test_bill.save()
        response = self.client.post(reverse('imaging_system_app:bills'),
                                            data={'bill_customer': 'test2',
                                                  'bill_from': '2022-10-10',
                                                  'bill_to': '2022-12-12'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "2")
        self.assertContains(response, "test2")
        self.assertEquals(len(response.context['bills']), 1)

    def test_bill_queries_non_existent(self):
        create_superuser(self)
        test_customer = add_customer("test_customer")
        other_test_customer = add_customer("test2")
        first_test_bill = add_bill(test_customer)
        second_test_bill = add_bill(other_test_customer)
        response = self.client.post(reverse('imaging_system_app:bills'),
                                            data={'bill_customer': 'not-yet-billed'})
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "There are no bills present.")
        self.assertEquals(len(response.context['bills']), 0)

# ===================== HELPER FUNTCTIONS =====================  #
def add_service(name, price, unit_name):
    service = Services.objects.create(name=name,
                                      normal_price=price,
                                      external_price = price*1.5,
                                      unit_name = unit_name)
    
    service.save()
    return service

def add_customer(cust_name):
    customer = Customer.objects.create(cust_name = cust_name,
                                       cust_tel_no = "123456789101",
                                       cust_email = "email@email.com",
                                       cust_budget_code = 101,
                                       cust_type = 1.0)
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

def add_worker(test_name, customer):
    worker = Worker.objects.create(worker_name = test_name,
                                   worker_tel_no = "123456789",
                                   worker_email = "worker@email.com",
                                   cust_id = customer)
    return worker
def add_bill(customer):
    new_bill = Bill.objects.create(billing_address = "Fake Street 6",
                                   total_cost = 20,
                                   cust_id = customer)
    return new_bill
