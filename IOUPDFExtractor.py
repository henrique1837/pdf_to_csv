# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 17:48:10 2020

@author: henrique
"""


# importing all the required modules
import os
import PyPDF2
import pandas as pd
import glob


def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

path = "/home/henrique/Documents/ltpn/pdf_to_csv"
os.chdir(path)


if not os.path.exists('./pdf'):
    os.makedirs('./pdf')
if not os.path.exists('./csv'):
    os.makedirs('./csv')


# creating an object 
pdfs = glob.glob("./pdf/*.pdf")
for k in range(len(pdfs)):
    print("File "+str(k+1)+" from "+str(len(pdfs)))
    file = open(pdfs[k], 'rb')
    
    
    # creating a pdf reader object
    fileReader = PyPDF2.PdfFileReader(file)
    
    
    totalPages = fileReader.getNumPages()
    pages = []
    
    for i in range(totalPages):
        pageObj = fileReader.getPage(i)
        if(i < totalPages -1):
            pages.append(pageObj.extractText().split("Data File",1)[0].split("|-------|----|-------|----------|----------|--------|",1)[1])
        else:
            pages.append(pageObj.extractText().split("Totals :",1)[0].split("|-------|----|-------|----------|----------|--------|",1)[1])
    
    table_arr = ''.join(pages).split()
    
    treated_table_arr = []
    i = 0
    while i < len(table_arr):
        if(isfloat(table_arr[i])==False and isfloat(table_arr[i+1])==False):
            treated_table_arr.append(table_arr[i]+" "+table_arr[i+1])
            i = i + 2
        else:
            treated_table_arr.append(table_arr[i])
            i = i + 1
        
    columns = 7
    i = 0
    df = pd.DataFrame({
        "peak": [],
        "ret_time": [],
        "type": [],
        "width": [],
        "area": [],
        "height": [],
        "area_p": []
    })
    while i < len(treated_table_arr):
        peak = treated_table_arr[i]
        ret_time = treated_table_arr[i+1]
        typ = treated_table_arr[i+2]
        width = treated_table_arr[i+3]
        area = treated_table_arr[i+4]
        height = treated_table_arr[i+5] 
        area_p = treated_table_arr[i+6]
        i = i + columns
        df = df.append({
            "peak": peak,
            "ret_time": ret_time,
            "type": typ,
            "width": width,
            "area": area,
            "height": height,
            "area_p": area_p
        },ignore_index=True)
    # print the number of pages in pdf file
    csv_file = "./csv/"+pdfs[k].split("pdf/",1)[1].replace('pdf','csv')
    df.to_csv(csv_file,sep=";")
