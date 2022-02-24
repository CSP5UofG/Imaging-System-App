from imaging_system_app.models import Customer, Worker, Services, Bill, ProjectServicesBridge, ProjectBillBridge, Project, WorkerProjectBridge

import pandas as pd
from os import listdir
import numpy as np
import seaborn as sns
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def create_plots():
    projects = Project.objects.all()
    all_projects = pd.DataFrame(list(projects.values()))
    
    all_customers = Customer.objects.all()
    customers_df = pd.DataFrame(list(all_customers.values()))[['cust_id', 'cust_name']]
    
    projects_with_cust_names = customers_df.merge(all_projects, left_on='cust_id', right_on="cust_id_id")
        
    myplot = sns.countplot(data=projects_with_cust_names,
                         x="cust_name")
    myplot.set_title("Number of projects per customer")
    myplot.set_xlabel("Customer ID")
    myplot.set_ylabel("Total number of projects")
    plt.close()
    fig = myplot.get_figure()
    fig.savefig('static/images/fig1.png') 
    
    myplot2 = sns.barplot(data=projects_with_cust_names,
                         x = 'cust_name',
                         y = 'total')
    myplot2.set_title('Average project cost per customer')
    myplot2.set_xlabel("Customer ID")
    myplot2.set_ylabel("Average project cost")
    plt.close()
    fig2 = myplot2.get_figure()
    fig2.savefig('static/images/fig2.png') 
    
