import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

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

#Attribute Anzeigen rechnen


#Anzeige Browser

if onOverall:
    st.title("Nährwerttabelle existiert")
    chart_data = pd.DataFrame({
    'Nährwert Tabelle vorhanden': ["ja","nein"],
    'Anzahl Produkte':[countJa,countNe]
    })
    c = ( 
        alt.Chart(chart_data).mark_bar().encode(x='Nährwert Tabelle vorhanden',y='Anzahl Produkte')
        )
    st.altair_chart(c, use_container_width=True)

if onAttribute:
    
    st.title("Nährwerte pro Produkte")

    @st.cache_data(ttl=600)
    def get_data_cal():
        db = client.mydb
        items = db.mycollection.find({"product_data.nutrition_table.calories":{"$exists":"true"}},{"_id": 0, "product_data" :{ "nutrition_table" : 1} })
        items = list(items)
        return items

    calItem = get_data_cal()

    countCal = 0
    for item in calItem:
        countCal += 1
    st.write("- Kalorien gespeichert bei :" , countCal , "Produkten")

    @st.cache_data(ttl=600)
    def get_data_carbo():
        db = client.mydb
        items = db.mycollection.find({"product_data.nutrition_table.carbohydrate_content":{"$exists":"true"}},{"_id": 0, "product_data" :{ "nutrition_table" : 1} })
        items = list(items)
        return items

    carbItem = get_data_carbo()

    countCarb = 0
    for item in carbItem:
        countCarb += 1
    st.write("- Products with carbohydrate_content shown:" , countCarb)

    @st.cache_data(ttl=600)
    def get_data_fat():
        db = client.mydb
        items = db.mycollection.find({"product_data.nutrition_table.fat_content":{"$exists":"true"}},{"_id": 0, "product_data" :{ "nutrition_table" : 1} })
        items = list(items)
        return items

    fatItem = get_data_fat()

    countfat = 0
    for item in fatItem:
        countfat += 1
    st.write("- Products with fat_content shown:" , countfat)

    @st.cache_data(ttl=600)
    def get_data_fib():
        db = client.mydb
        items = db.mycollection.find({"product_data.nutrition_table.fiber_content":{"$exists":"true"}},{"_id": 0, "product_data" :{ "nutrition_table" : 1} })
        items = list(items)
        return items

    fibItem = get_data_fib()

    countfib = 0
    for item in fibItem:
        countfib += 1
    st.write("- Products with fiber_content shown:" , countfib)

    @st.cache_data(ttl=600)
    def get_data_prot():
        db = client.mydb
        items = db.mycollection.find({"product_data.nutrition_table.protein_content":{"$exists":"true"}},{"_id": 0, "product_data" :{ "nutrition_table" : 1} })
        items = list(items)
        return items

    protItem = get_data_prot()

    countprot = 0
    for item in protItem:
        countprot += 1
    st.write("- Products with protein_content shown:" , countfib)

    diaOn = st.toggle("Show Diagramm")

    if diaOn : 
        chart_data = pd.DataFrame({
            'Nährwerte': ["Kalorien","Carbonhydrate", "Fette" , "Fiber", "Proteine"],
            'Anzahl Produkte':[countCal,countCarb,countfat,countfib,countprot]            })
        c = ( 
            alt.Chart(chart_data).mark_bar().encode(x='Nährwerte',y='Anzahl Produkte')
        )
        st.altair_chart(c, use_container_width=True)