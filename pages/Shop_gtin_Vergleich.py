import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import array

onOverall = st.sidebar.toggle("Zeige Übereinstimmungen von gleichen Produkten in mehreren Shops",value=True)

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

items = get_data_gtin()

# mehr als 2 shops

if len(options) >= 2 :
    numShop = len(options)
    urls = ["https://www.edeka24.de/","https://www.vekoop.de/"]

    arr0 = []
    arr1 = []
    arr2 = []
    arr3 = []
    arr4 = []
    arr5 = []
    arr6 = []

    arrSame0 = []
    arrSame1 = []

    for i in range(numShop) : 
        for item in items :
            if i == 0 :
                if item["shop_url"] == urls[i] and options[i] == "Edeka":
                  arr0.append(item["product_data"]["gtin"])
                if item["shop_url"] == urls[i] and options[i] == "Vekoop":
                  arr0.append(item["product_data"]["gtin"])
            if i == 1 :
                if item["shop_url"] == urls[i] and options[i] == "Edeka":
                  arr1.append(item["product_data"]["gtin"])
                if item["shop_url"] == urls[i] and options[i] == "Vekoop":
                  arr1.append(item["product_data"]["gtin"])

    if len(options) == 2 :
        for a in range(len(arr0)):
            for b in range(len(arr1)) :
                if arr0[a] == arr1[b] :
                    arrSame0.append(arr0[a])
                    arrSame1.append(arr1[b])

    st.subheader("Diese Produkte gibt es in beiden Geschäften")

    first = st.checkbox(options[0])
    second = st.checkbox(options[1])

    col1, col2 = st.columns(2)

    with col1:
        if first :
            st.subheader(options[0], ":")
            for item in items :
                for i in range(len(arrSame0)) :
                    if item["shop_url"] == urls[0] and item["product_data"]["gtin"] == arrSame0[i] :
                        st.write("- ", item["product_data"]["name"])

    with col2:
        if second:
            st.subheader(options[1], ":")
            for item in items :
                for i in range(len(arrSame1)) :
                    if item["shop_url"] == urls[1] and item["product_data"]["gtin"] == arrSame1[i] :
                        st.write("- ", item["product_data"]["name"])



