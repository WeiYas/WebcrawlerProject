import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

onOverall = st.sidebar.toggle("Zeige Diagramm von Produkten mit gtin",value=True)

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()

# ------ Produkte Gtin ja nein ----------

@st.cache_data(ttl=600)
def get_data_gtinJa():
    db = client.mydb
    items = db.mycollection.find({"product_data.gtin":{"$exists":"true"}}, {"_id" :0 , "product_data" : {"gtin" : 1}})
    items = list(items)
    return items

gtinJa = get_data_gtinJa()

@st.cache_data(ttl=600)
def get_data():
    db = client.mydb
    items = db.mycollection.find({}, {"_id" :1})
    items = list(items)
    return items

gtinNein = get_data()

countGtin = 0
countNogtin = 0
count = 0
for item in gtinJa:
    countGtin += 1

for item in gtinNein :
    count += 1

countNogtin = count - countGtin
# st.write(countGtin)

chart_data = pd.DataFrame({
  'Gtin vorhanden': ["ja","nein"],
  'Anzahl Produkte':[countGtin,countNogtin]
})



# ANZEIGE AUF BROWSER

st.title("Produkte mit Gtin")
st.write(" ")

if onOverall :
    st.subheader("Wieviele Produkte besitzen einen gtin?")
    st.write("Anzahl von Produkten mit gtin: ", countGtin)
    st.write("Anzahl von Produkten ohne gtin" , countNogtin)
    #chart_data = chart_data.set_index('Gtin vorhanden')
    #st.bar_chart(chart_data)
    c = ( 
    alt.Chart(chart_data).mark_bar().encode(x='Gtin vorhanden',y='Anzahl Produkte')
    )
    st.altair_chart(c, use_container_width=True)