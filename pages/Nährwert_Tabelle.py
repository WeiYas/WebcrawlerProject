import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

st.title("Nährttabelle existiert")

onOverall = st.sidebar.toggle("Nährwert Vorhanden",value=True)
onAttribute = st.sidebar.toggle("Attribute ausgefüllt")

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()

@st.cache_data(ttl=600)
def get_data_tableJa():
    db = client.mydb
    items = db.mycollection.find({"product_data.nutrition_table":{"$exists":"true"}} , {"_id": 1})
    items = list(items)
    return items

@st.cache_data(ttl=600)
def get_data():
    db = client.mydb
    items = db.mycollection.find({},{"_id": 1})
    items = list(items)
    return items

tableJa = get_data_tableJa()
tableAll = get_data()
count = 0
countJa = 0
countNe = 0

for i in tableJa :
    countJa += 1

for i in tableAll : 
    count += 1

countNe = count - countJa

#Attribute Anzeigen


#Anzeige Browser

if onOverall:
    chart_data = pd.DataFrame({
    'Nährwert Tabelle vorhanden': ["ja","nein"],
    'Anzahl Produkte':[countJa,countNe]
    })
    c = ( 
        alt.Chart(chart_data).mark_bar().encode(x='Nährwert Tabelle vorhanden',y='Anzahl Produkte')
        )
    st.altair_chart(c, use_container_width=True)