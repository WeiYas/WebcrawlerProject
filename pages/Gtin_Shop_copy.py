import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import array
import plotly.graph_objects as go

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()

st.title("Produkte mit GTIN")
st.markdown('<style>h1{font-size:25px;} h3{font-size:20px;}</style>', unsafe_allow_html=True)

    # ------ Produkte Gtin ja ----------

#st.write(len(options))

#SHOPS
@st.cache_data(ttl=600,show_spinner = False)
def get_data():
    db = client.mydb
    items = db.all_flatten.find({},{"shop_url":1, "product_data/gtin":1})
    items = list(items)
    return items

@st.cache_data(ttl=600,show_spinner = False)
def get_data_no_flatten() :
    db = client.mydb
    items = db.mycollection.find({"completeness" : {"$exists" : True}},{"_id":0, "completeness":1, "shop_url" : 1})
    items = list(items)
    return items

items = get_data()
#items_noflatten = get_data_no_flatten()

count_dict_url = {}
count_dict_complete = {}

for key in items :
    if key["shop_url"] not in count_dict_url :
        count_dict_url[key["shop_url"]] = 1
    else:
        count_dict_url[key["shop_url"]] += 1

#print(count_dict_complete)

url_list = list(count_dict_url)
complete_list = list(count_dict_complete)

shopsName = []
produkteAnzahl = []
completenessAnzahl = []

for item in range(len(url_list)) : 
    shopsName.append(url_list[item])

options = st.multiselect(
    "Wähle Geschäfte und zeige welche Produkte in diesen gleichzeitig zur Verfügung stehen",
    shopsName)
st.write("Nur Produkte mit registriertem GTIN können angezeigt werden")

# mehr als 2 shops

if len(options) == 2 :
    with st.spinner('Daten werden geladen...'):

        
        numShop1, numShop2 = 0,0

        print(" ")
        print(shopsName)
        print(" ")
        print(options)
        print(" ")

        for i in range(len(options)) : 
            for s in range(len(shopsName)) :
                if options[0] == shopsName[s] :
                    numShop1 = options[0]
                if options[1] == shopsName[s] :
                    numShop2 = options[1]

        print("Shops:" , numShop1, " and ",numShop2)
        print(" ")

        arr1, arr2 = [], []     
        arrSame1,arrSame2 = [],[]
        name0, name1 = [] , []


        for i in range(len(options)):
            for item in items :
                if item["shop_url"] == numShop1 and options[i] == numShop1 :
                    arr1.append(item["product_data/gtin"])

                elif item["shop_url"] == numShop2 and options[i] == numShop2 :
                    arr2.append(item["product_data/gtin"])

        

        for i in range(len(shopsName)) :
            if options[0] == numShop1 and options[1] == numShop2 or  options[1] == numShop1 and options[0] == numShop2:
                for a in range(len(arr1)):
                    for b in range(len(arr2)) :
                        if arr1[a] == arr2[b] :
                            arrSame1.append(arr1[a])
                            arrSame2.append(arr2[b])

        print("FirstARR:" ,arr1)
        print("SecondARR:", arr2)

        lenG = len(arrSame1)
       
        st.subheader("Diese Produkte gibt es in beiden Geschäften")
        #print(arrSameE)
        #print(arrSameG)
        
        st.write("Anzahl gleicher Produkte: " ,str(lenG))




            



