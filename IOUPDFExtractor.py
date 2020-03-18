# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 17:48:10 2020

@author: henrique
"""


# importing all the required modules
import PyPDF2
import pandas as pd

# creating an object 
file = open('/home/henrique/Downloads/DIC07_20_03_0022_.pdf', 'rb')


# creating a pdf reader object
fileReader = PyPDF2.PdfFileReader(file)


pageObj = fileReader.getPage(0)
p1_page = pageObj.extractText().split("Data File",1)[0].split("|-------|----|-------|----------|----------|--------|",1)[1]
pageObj = fileReader.getPage(1)
p2_page = pageObj.extractText().split("Totals :",1)[0].split("|-------|----|-------|----------|----------|--------|",1)[1]

table_arr = (p1_page + p2_page).split()
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
while i < len(table_arr):
    peak = table_arr[i]
    ret_time = table_arr[i]
    width = table_arr[i+1]
    typ = table_arr[i+2]
    area = table_arr[i+3]
    height = table_arr[i+4] 
    area_p = table_arr[i+5]
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
    
df.to_csv("/home/henrique/Downloads/iou.csv",sep=";")
