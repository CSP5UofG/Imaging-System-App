import sqlite3
from xlsxwriter.workbook import Workbook

def create_excel():
    #creayte new excle file
    workbook = Workbook('resources/excel/ExcelDatabase.xlsx')
    
    #set up connection and cursor for the required database
    conn=sqlite3.connect('db.sqlite3')
    c=conn.cursor()
    
    #get all table names
    sql_query = """SELECT name FROM sqlite_master  
      WHERE type='table';"""
    tables = c.execute(sql_query).fetchall()
    
    for tups in tables:
        #select for related tables only
        if tups[0].startswith("imaging"):
            #add new worksheet named aftre the table
            worksheet = workbook.add_worksheet(str(tups[0])[19:])
            
            #set up query to extract all data
            query = "select * from " + str(tups[0])
            c.execute(query)
            mysel=c.execute(query)
            
            #write header - column names in first row
            counter = 0
            for tup in c.description:
                worksheet.write(0, counter, tup[0])
                counter+=1
            
            #write data into corresponding cells
            for i, row in enumerate(mysel):
                for j, value in enumerate(row):
                    worksheet.write(i+1, j, row[j])
    
    workbook.close()
