import pandas as pd 
import matplotlib.pyplot as plt 
import seaborn as sns
from bs4 import BeautifulSoup
from requests import get

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

app = Flask(__name__)

@app.route("/")
def home():
    return get_data()
    
if __name__ == "__main__":
    app.run(debug=True)




