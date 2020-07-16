import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
from bs4 import BeautifulSoup
from requests import get
import csv
from flask import Flask


def get_data():
    url = "https://www.mygov.in/corona-data/covid19-statewise-status/"
    response = get(url)
    html_soup = BeautifulSoup(response.text, 'html.parser')
    html_soup=html_soup.find_all("div",class_="field field-name-field-covid-statewise-data field-type-field-collection field-label-above")[0]
    html_soup=html_soup.find_all("div",class_="field-items")[0]
    html_soup=html_soup.find_all("div",class_="entity entity-field-collection-item field-collection-item-field-covid-statewise-data clearfix")
    arr=dict()
    for i in html_soup:
        name = i.find("div",class_="field-item even").text
        death = int(i.find("div",class_="field field-name-field-deaths field-type-number-integer field-label-above").find("div",class_="field-item even").text)
        cured = int(i.find("div",class_="field field-name-field-cured field-type-number-integer field-label-above").find("div",class_="field-item even").text)
        total = int(i.find("div",class_="field field-name-field-total-confirmed-indians field-type-number-integer field-label-above").find("div",class_="field-item even").text)
        print(name," ",total," ",cured," ",death)
        #arr+=[[name,total,cured,death]]
        arr[name]={"total":total,"cured":cured,"death":death}
    return (arr)

reader = csv.reader(open("state.csv", 'r'))
d={}

for row in reader:
    d[row[0]]= {"name": row[1],"total": int(row[2]),"cured": int(row[3]),"death": int(row[4])}
print(d)

def graph_plt(z):
    s=str(z)
    a=d[s]
    nm,total,cured,death=a['name'],a['total'],a['cured'],a['death']
    infected=total-cured-death
    print(nm,total,cured,death)
    # --- dataset 1: just 4 values for 4 groups:
    fig, ax = plt.subplots()
    plt.rcParams['font.sans-serif'] = 'Arial'
    plt.rcParams['font.family'] = 'sans-serif'
    plt.rcParams['text.color'] = '#909090'
    plt.rcParams['axes.labelcolor']= '#909090'
    plt.rcParams['xtick.color'] = '#909090'
    plt.rcParams['ytick.color'] = '#909090'
    plt.rcParams['font.size']=12
    plt.title(nm)
    labels = ['Dead', 
            'Cured', 'infected']
    percentages = [death*100/total, cured*100/total,infected*100/total]
    explode=(0.1,0,0)
    ax.pie(percentages, explode=explode, labels=labels,  
         autopct='%1.0f%%', 
        shadow=False, startangle=0,   
        pctdistance=1.2,labeldistance=1.4)

    ax.legend(frameon=False, bbox_to_anchor=(1.5,0.8))

 
    
    plt.show()
graph_plt(20)

