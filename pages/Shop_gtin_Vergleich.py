import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import array

onOverall = st.sidebar.toggle("Zeige Diagramm von Produkten mit gtin",value=True)

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()

# ------ Produkte Gtin ja ----------

options = st.multiselect(
    "Wähle Geschäfte und zeige welche Produkte in diesen gleichzeitig zur Verfügung stehen",
    ["Edeka", "Vekoop"])
st.write("Nur Produkte mit registriertem gtin können angezeigt werden")
st.write(len(options))

@st.cache_data(ttl=600)
def get_data_gtin():
    db = client.mydb
    items = db.mycollection.find({"product_data.gtin":{"$exists":"true"}}, {"_id" :0 , "product_data" : {"name" : 1 ,"gtin" : 1}, "shop_url":1})
    items = list(items)
    return items

if len(options) == 2:
    items = get_data_gtin()
    arrE = []
    arrV = []

    for i in items :
        if i["shop_url"] == "https://www.edeka24.de/" and options[0] == "Edeka":
            arrE.append(i["product_data"]["gtin"])
    for i in items :
        if i["shop_url"] == "https://www.vekoop.de/" and options[1] == "Vekoop":
            arrV.append(i["product_data"]["gtin"])

    #all = []
    #all = arrE + arrV
    #all.sort()


    arrSameGEd = []
    arrSameGVe = []


    for a in range(len(arrE)):
        for b in range(len(arrV)) :
            if arrE[a] == arrV[b] :
                arrSameGEd.append(arrE[a])
                arrSameGVe.append(arrV[b])

    #st.write(arrSameG)

    st.subheader("Diese Produkte gibt es in beiden Geschäften")

    first = st.checkbox(options[0])
    second = st.checkbox(options[1])

    col1, col2 = st.columns(2)

    with col1:
        if first :
            st.subheader(options[0], ":")
            for item in items :
                for i in range(len(arrSameGEd)) :
                    if item["shop_url"] == "https://www.edeka24.de/" and item["product_data"]["gtin"] == arrSameGEd[i] :
                        st.write("- ", item["product_data"]["name"])

    with col2:
        if second:
            st.subheader(options[1], ":")
            for item in items :
                for i in range(len(arrSameGVe)) :
                    if item["shop_url"] == "https://www.vekoop.de/" and item["product_data"]["gtin"] == arrSameGVe[i] :
                        st.write("- ", item["product_data"]["name"])


# mehr als 2 shops


