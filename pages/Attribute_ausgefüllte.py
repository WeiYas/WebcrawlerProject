import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import plotly.express as px

st.title("Verteilung Attribute ausgefüllt")
st.write(" ")
onProduktverteilungGtin = st.sidebar.toggle("Ausgefüllte Attribute Anzeige")

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()

# ----- Produkte Completeness -------

@st.cache_data(ttl=600)
def get_data():
    db = client.mydb
    items = db.mycollection.find({}, {"_id" :0, "completeness" : 1})
    items = list(items)
    return items

item = get_data()

count1 = 0
count2= 0
count3 = 0
count4 = 0
count5 = 0
count6 = 0
count7 = 0
count8 = 0
count9 = 0
count10 = 0

for items in item:
    if items["completeness"] <= 0.1 and items["completeness"] > 0.0 :
        count1 +=1     
    if items["completeness"] <= 0.2 and items["completeness"] > 0.1 :
        count2 +=1     
    if items["completeness"] <= 0.3 and items["completeness"] > 0.2 :
        count3 +=1
    if items["completeness"] <= 0.4 and items["completeness"] > 0.3 :
        count4 +=1     
    if items["completeness"] <= 0.5 and items["completeness"] > 0.4 :
        count5 +=1     
    if items["completeness"] <= 0.6 and items["completeness"] > 0.5 :
        count6 +=1     
    if items["completeness"] <= 0.7 and items["completeness"] > 0.6 :
        count7 +=1
    if items["completeness"] <= 0.8 and items["completeness"] > 0.7 :
        count8 +=1
    if items["completeness"] <= 0.9 and items["completeness"] > 0.8 :
        count9 +=1
    if items["completeness"] <= 1 and items["completeness"] > 0.9 :
        count10 +=1

if onProduktverteilungGtin :
    chart_data = pd.DataFrame({'name': ["0.0 - 0.1","0.1 - 0.2", "0.2 - 0.3","0.3 - 0.4", "0.4 - 0.5", "0.5 - 0.6", "0.6 - 0.7", "0.7 - 0.8" , "0.8 - 0.9" , "0.9 - 1.0"], 'number of products':[count1,count2,count3,count4,count5,count6,count7,count8,count9,count10]})
    chart_data = chart_data.set_index('name')
    st.bar_chart(chart_data)
    fig = px.bar