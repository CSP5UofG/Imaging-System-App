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
    projects_with_cust_names['year'] = projects_with_cust_names.apply(add_year, axis=1)
    projects_with_cust_names['month'] = projects_with_cust_names.apply(add_month, axis=1)
    
    myplot = sns.countplot(data=projects_with_cust_names,
                         x="cust_name")
    myplot.set_title("Number of projects per customer")
    myplot.set_xlabel("Customer name")
    myplot.set_ylabel("Total number of projects")
    plt.close()
    fig = myplot.get_figure()
    fig.savefig('resources/images/fig1.png') 
    
    myplot2 = sns.barplot(data=projects_with_cust_names,
                         x = 'cust_name',
                         y = 'total')
    myplot2.set_title('Average project cost per customer')
    myplot2.set_xlabel("Customer name")
    myplot2.set_ylabel("Average project cost")
    plt.close()
    fig2 = myplot2.get_figure()
    fig2.savefig('resources/images/fig2.png') 
    
    monthly_sum = projects_with_cust_names[['cust_name', 'project_id', 'year', 'month', 'project_date']]
    counted = monthly_sum.groupby(['year', 'month'], as_index=True)["project_id"].count().reset_index(name="count")
    counted = counted.sort_values(['year', 'month']).tail(12)
    max_project_count = int(counted['count'].max())
    ticks = np.arange(0, max_project_count+1, 1)
    myplot3 = sns.lineplot(data = counted,
                           x = 'month',
                           y = 'count')
    myplot3.set_title('Monthly trend of project numbers from the last 12 months')
    myplot3.set_xlabel("Month")
    myplot3.set_ylabel("Number of porjects")
    plt.yticks(ticks)
    plt.close()
    fig3 = myplot3.get_figure()
    fig3.savefig('resources/images/fig3.png') 

    
def add_year(row):
    date = str(row['project_date'])
    return date[0:4]

def add_month(row):
    date = str(row['project_date'])
    return date[5:7]