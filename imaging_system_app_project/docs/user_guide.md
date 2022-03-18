# User Guide
  * [Registration and login](#registration-and-login)
  * [Services](#services)
  * [Customers](#customers)
  * [Projects](#projects)
  * [Bills](#bills)
  * [Statistics](#statistics)
  * [Extra resources for admins](#extra-resources-for-admins)


## Registration and login

### Registration
- On the login page, there is a register button next to login to redirect you to the registration page. 
- Type in your desired username and password then press the register button.
- Wait for the admin to activate your account before logging in.
- For admins: (refer to the [moderating user accounts](#moderating-user-accounts) section in Extra resources for admins for details)
  - To activate a user account, login to the admin page using your admin account, default on site_page/admin/
  - Navigate to Users under Authentication and Authorization.
  - Select the tickbox of the account you would like to activate.
  - In the dropdown menu, select Activate user and press the go button.
  - The user account is now activated and can be used to log in to the site.
  - The dropdown menu also contains options to deactivate user accounts, and grant or revoke permission for the accounts to use the admin site.

### Login
- By default, all pages requiring logging in will redirect to the login page.
- Enter your account details and press Login, you will be redirected to the home page.
- The home page shows the 5 most recently created projects and bills.
- The logout button is at the left-bottom corner of the page.


## Services

### Viewing services
- Press the Services tab on the left of the page, the list of services will be shown, with their normal price and external price.
- The search button allows searching for services by their name.
  - Type in the name of the service you would like to find and press the search button.
  - All services matching your search string will show up.
  - To view all services again, either press the Services tab or clear the search box and press the search button again.

### Adding a new service
- Press the New Service button on the top of the Services page.
- Fill in the name of the service, the normal price of the service and the unit name of the service.
  - For example, the unit name for a microscope can be hour and a process can be sample or run.
- Press the Create New Service button after filling in the form. The external price of the service is automatically calculated with a default multiplier of 1.5.
- You will be redirected back to the Services page, and the new service will show up in the list.

### Editing a service
- On the Services page, press the Edit button next to the service you would like to edit.
- Press the Update Service button after making changes. The external price will be automatically updated.
- You will be redirected back to the Services page and the service in the list of services is now updated.


## Customers

### Viewing customers
- Press the Customers tab on the left of the page, the list of customers will be shown.
- To view the details of a customer, press the View button next to that customer.
  - The customer details and the workers, projects, and bills associated to the customer are shown.
- The search button allows searching for customers by their details.
  - Type in the details of the customer you would like to find and press the search button.
  - All customers matching your search string will show up.
  - To view all customers again, either press the Customers tab or clear the search box and press the search button again.

### Adding a new customer
- Press the New Customer button on the top of the Customers page.
- Fill in the form and select the customer type.
  - The customer type dictates whether a customer will be billed using the normal or external price.
- Press the Create New Customer button. You will be redirected back to the Customers page, and the new customer will show up in the list.

### Editing a customer
- On the Customers page, press the Edit button next to the customer you would like to edit.
- Press the Update Customer button after making changes, you will be redirected back to the details page of the customer.

### Adding a worker for a customer
- Navigate to the customer details page of the customer associated with the worker.
- Press the Add Worker button and fill in the form.
- Press the Add Worker button. You will be redirected back to the customer details page, and the new worker will show up in the list.

### Editing a worker
- Navigate to the customer details page of the customer associated with the worker
- Press the Edit button next to the worker you would like to edit.
- Press the Update Customer button after making changes, you will be redirected back to the details page of the customer.

## Projects

### Viewing projects
- Press the Projects tab on the left of the page, the list of projects will be shown.
- To view the details of a project, press the View button next to that project.
- The search button allows searching for projects by their customer's name.
  - Type in the name of the customer you would like to find and press the search button.
  - All projects with a customer matching your search string will show up.
  - To view all projects again, either press the Projects tab or clear the search box and press the search button again.
- The date filter allows searching for the project date of the projects within a specific date range.
  - Press the calendar icon in the From and To fields to set the date range then press the search button. Note that you can also set only one of them to filter out all dates before or after the specified date.
  - The date filter can also be combined with the customer search.
  - To reset the filter, press the Projects tab.

### Adding a new project
- Note that you should have already created the customer and worker associated with the project.
- Press the New Project button on the top of the Projects page.
- Select the customer of the project from the dropdown list. Note that the dropdown list is ordered by the customer name. However, typing the customer name while having the dropdown list open will change the highlighted customer to the typed in text.
  - In practice, open the dropdown list and type in the customer name to automatically highlight the customer, instead of scrolling through a potential long list of customers.
- Select the worker from the dropdown list. The list of workers are associated to the selected customer.
- To add more workers to the project, press the Assign more workers button.
- In the specimen preparation record form, the rest of the fields below the field for the number of samples are optional.
- Select the service and fill in the unit field. For example, 1 hour usage of the microscope is 1.0.
  - Units for microscope usage allows for 0.5 increments (30 minutes), while processes units must be integers.
  - To add more services to the project, press the Add another service button.
- Press the Create New Project button. You will be redirected back to the Projects page.
- The project cost will be automatically calculated and the new project will show up in the list.

### Editing a project
- On the Projects page, press the Edit button next to the project you would like to edit.
- Press the Update Project button after making changes, the project cost will be automatically updated and you will be redirected back to the details page of the project.


## Bills

### Viewing bills
- Press the Bills tab on the left of the page, the list of bills will be shown.
- To view the details of a bill, press the View button next to that bill.
- The search button allows searching for bills by their customer's name.
  - Type in the name of the customer you would like to find and press the search button.
  - All bills with a customer matching your search string will show up.
  - To view all bills again, either press the Bills tab or clear the search box and press the search button again.
- The date filter allows searching for the billing date of the bills within a specific date range.
  - Press the calendar icon in the From and To fields to set the date range then press the search button. Note that you can also set only one of them to filter out all dates before or after the specified date.
  - The date filter can also be combined with the customer search.
  - To reset the filter, press the Bills tab.

### Adding a new bill
- Note that you should have already created the projects associated with the bill.
- Press the New Bill button on the top of the Bills page.
- Select the customer of the project from the dropdown list. Note that the dropdown list is ordered by the customer name. However, typing the customer name while having the dropdown list open will change the highlighted customer to the typed in text.
  - In practice, open the dropdown list and type in the customer name to automatically highlight the customer, instead of scrolling through a potential long list of customers.
- Select the project from the dropdown list. The list of projects are associated to the selected customer and are sorted by the project date.
  - To add more projects to the bill, press the Bill more projects button.
- The remaining fields in the form allows specifying a billing address and up to 2 extra services and their cost.
- Press the Create New Bill button. You will be redirected back to the Bills page.
- The billing cost will be automatically calculated and the new bill will show up in the list.

### Editing a bill
- On the Bills page, press the Edit button next to the bill you would like to edit.
- Press the Update Bill button after making changes, the billing cost will be automatically updated and you will be redirected back to the details page of the bill.

### Printing a bill
- On the Bills page, press the Print button next to the bill you would like to print.
- You will be redirected to a pdf version of the bill that you can save and print.
  - Alternately, this may be a prompt to download the pdf instead of the redirect.
- To go back to the website, use the back button of the browser.


## Statistics

### Viewing Statistics
- Press the Statistics tab on the left of the page, graphs of the statistics will be shown.

### Downloading the database
- On the Statistics page, Press the Download Database button on the top of the Bills page.
- You will be prompted to download an excel file of the database.
- The worksheets in the database corresponds to the database structure as follows:
  - bill: Object containing entries for bills.
  - customer: Object containing entries for customers.
  - projectbillbridge: Object containing entries for which projects are contained in a bill.
  - projectservicesbridge: Object containing entries for which services are contained in a project with the calculated price.
  - project: Object containing entries for projects.
  - service: Object containing entries for services.
  - workerprojectbridge: Object containing entries for which workers are associtated with a project.
  - worker: Object containing entries for workers.


----------------------------

# Extra resources for admins

- The admin site, default in site_name/admin , allows moderating user accounts and fine-grained changes to the database.

- After logging in, the left top corner contains a link for changing the admin password.

- The left top corner also contains a link to a more technical documentation of the site.

## Caution
**It is generally not recommended to make changes to the database in the admin site. Since validation of data is not done in the admin site, removing required fields in entries may cause the database to crash, and the database will need to be reloaded, effectively losing all the data in the website, although the data can still be exported using command prompt.**
- To make changes to the database, select the object you would like to change.
  - Press the blue highlighted name of the entry to edit its details.
  - To delete an entry, select its checkbox. In the dropdown list at the top, select delete selected entry and press the Go button. 
- If the database crashes:
  - Export the data using command prompt
    - Open a command prompt and navigate to the project directory
      - Refer to the how to install section of readme.md for instructions.
    - Type in the following command:
      - `py manage.py dumpdata > data.json`
    - The database is now exported as a json file which can be found in the project directory.
  - To reload the database:
    - Delete db.sqlite3 in the project folder
    - Follow the instructions in the how to install section of readme.md starting from the "Set up the database of the project" section.


## Moderating user accounts
- Select Users under Authentication and Authorization.
- Select user/users using the checkboxes.
- Select an option from the dropdown menu and press the Go button.
  - Activate user: Activates the selected user/users to allow login
  - Disable user: Removes the selected user/users permission to login
  - Give staff priveledges to use the admin site: Allows the selected user/users to use the admin site
  - Revoke staff priveledges to use the admin site: Removes the permission of selected user/users to use the admin site


## Database
**As mentioned [above](#caution), deleting required fields in entries can cause irreversible changes.**

### Bills
- Object containing entries for bills.

### Customers
- Object containing entries for customers.

### Project bill bridges
- Object containing entries for which projects are contained in a bill.

### Project services bridges
- Object containing entries for which services are contained in a project with the calculated price.

### Projects
- Object containing entries for projects.

### Services
- Object containing entries for services.

### Worker project bridges
- Object containing entries for which workers are associtated with a project.

### Workers
- Object containing entries for workers.
