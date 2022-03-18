# Imaging System App

* [Introduction](#introduction)
* [Main features](#main-features)
* [How to install](#how-to-install)


## Introduction

This web app is built using the Django framework for digitalising the workflow of documenting and billing of electron microscopy for the Glasgow Imaging Facility. It is a database system that saves all created projects and bills, and allows exporting the bill as a pdf file.


## Main features:

A user guide is available in docs/user_guide.md

### Login functionality
- Restricts content to be viewable and editable only by approved individuals.
- The admin page is used for approving account registrations.

### Home page
- Shows the 5 most recently created projects and bills.

### Customising services
- Allows defining a list of available services with normal and external prices.
- Allows searching for services by their name.

### Customers and workers
- Allows creating and editing customer and workers that are associated to projects.
- Allows searching for customers by their details.
- The customer details page allows an overview of projects and bills associated to the customer.

### Projects
- Allows creating, editing and viewing projects.
- Allows searching for projects by the customer name and filtering by the project creation date.
- Services used in the project are selected from the services list.
- Project cost is automatically calculated.

### Bills
- Allows creating, editing and viewing bills.
- Allows searching for bills by the customer name and filtering by the billing date.
- Projects that are billed are selected from the list of projects associated with the customer.
- Billing cost is automatically calculated.
- A pdf version of the bill can be created and downloaded.

### Statistics
- A dedicated page for graphs of created projects.
- An excel version of the database can be downloaded.


## How to install

### **Download the project and Python**

Download the source code as a zip file and unzip it, by default it should be csp5-main-master.zip. You should now have a folder called imaging_system_app_project inside the unzipped folder, this is the project folder.

Install [Python](https://www.python.org/downloads/release/python-3910/).

When running the Python installer, remember to check the boxes next to “Install launcher for all users (recommended)”.

For any errors with Python, check out the [official documentation](https://docs.python.org/3/using/windows.html) to set up Python on Windows.


### **Adding your website as an allowed host**

Open allowed_hosts.txt in the project folder and type in your hosting website on a new line.
- E.g. https​://www.imagingsystemapp.gla.ac.uk


### **Changing the secret key**

For security purposes, change the secret key in secret_key.txt in the project folder.

The secret key should preferably be at least 50 characters.


### **Create a virtual environment**

Open command prompt and type the following command, replacing project_name with your desired name:
- `py -m venv project-name`


### **Activate the virtual environment**

Type the following command in the command prompt, replacing project_name with your desired name:
- `project-name\Scripts\activate.bat`

Note that this command has to be run every time you start a new command prompt.


### **Navigate to the project directory**

Navigate to the project directory in the command prompt.

For example if the csp5-main-master folder is in the Desktop:
- `cd Desktop`
- `cd csp5-main-master`
- `cd imaging_system_app_project`

Note that the instructions below require you to be in the project directory in the command prompt.


### **Install required packages**

Type the following command in the command prompt:

- `py -m pip install -r requirements.txt`


### **Set up the database of the project**

Type the following commands in the command prompt:
- `py manage.py makemigrations imaging_system_app`
- `py manage.py migrate`


### **Set up static files of the project**

Type the following command in the command prompt:
- `py manage.py collectstatic`

Answer yes when prompted.

### **Create an admin account**

Type the following command in the command prompt:
- `py manage.py createsuperuser`

Enter your desired username and password, email can be omitted by pressing Enter when prompted.


### **Load in sample data**

Type the following command in the command prompt:
- `py population_script.py`


### **Testing the project for any issues**

Type the following command in the command prompt:
- `py manage.py test`

It should take a moment to run and the final output in the command prompt should be:

```
OK

Destroying test database for alias 'default'...
```


### **Running the project on a local server**

Type the following command in the command prompt:
- `py manage.py runserver`

The project can now be accessed by going to http​://127.0.0.1:8000/ 

The admin page can now be accessed by going to http​://127.0.0.1:8000/admin 

To stop the local server, type Ctrl+C in the command prompt.


### **The project should now be ready to be hosted on your website.**
