import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()

st.markdown('<style>h1{font-size:25px;} h3{font-size:20px;}</style>', unsafe_allow_html=True)
st.title("Anzahl Produkte in einer spezifischen Preisgruppe")

shop = st.sidebar.radio(
    "Wähle 1 Shop aus",
    ["Edeka", "Vekoop"],
    index=None,)

rangeS = st.slider('Wähle eine Preisrange aus', value = [0,500])

container = st.container(border=True)

@st.cache_data(ttl=600)
def get_data():
    db = client.mydb
    items = db.mycollection.find({"product_data.price":{"$exists":True}},{"product_data" : {"price":1 , "name" : 1},"shop_url":1})
    items = list(items)
    return items

items = get_data()
count = 0
countE = 0
countV = 0
arr = []

for i in range(len(items)) : 
    if items[i]["product_data"]["price"] :
        price = items[i]["product_data"]["price"]
        if int(float(price)) <= rangeS[1] and int(float(price)) >= rangeS[0] :
            count += 1

with container: 
    st.write("- **Ausgewählter Bereich:**", str(rangeS[0])," bis " , str(rangeS[1])," EUR")
    st.write("- **Anzahl Produkte in diesem Bereich:**", str(rangeS[0]) , " to ", str(rangeS[1]), "EUR is: ", str(count))

if shop == "Edeka" :
    countT = 0
    st.subheader(shop)
    for item in items :
        if item["shop_url"] == "https://www.edeka24.de/":
            priceE = item["product_data"]["price"]
            countT += 1
            if int(float(priceE)) <= rangeS[1] and int(float(priceE)) >= rangeS[0] :
                countE += 1
    st.write("Anzahl Produkte in Preiskategorie:", countE)
    chart_data = pd.DataFrame({'name': ["Ausgewählte","Totale Anzahl"], 'number of products':[countE,countT]})
    chart_data = chart_data.set_index('name')
    st.bar_chart(chart_data)


if shop == "Vekoop" :
    countT = 0
    st.subheader("Vekoop:")
    for item in items :
        if item["shop_url"] == "https://www.vekoop.de/":
            priceV = item["product_data"]["price"]
            countT += 1
            if int(float(priceV)) <= rangeS[1] and int(float(priceV)) >= rangeS[0] :
                countV += 1
    st.write("Anzahl Produkte in Preiskategorie:", countV)
    chart_data = pd.DataFrame({'name': ["Ausgewählte","Totale Anzahl"], 'number of products':[countV,countT]})
    chart_data = chart_data.set_index('name')
    st.bar_chart(chart_data)