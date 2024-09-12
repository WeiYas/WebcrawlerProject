import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

st.title("Completeness-Bereich je Shop")
st.write(" ")
st.markdown('<style>h1{font-size:25px;} h3{font-size:20px;}</style>', unsafe_allow_html=True)

@st.cache_resource
def init_connection():
    return pymongo.MongoClient("mongodb://localhost:27017/")

client = init_connection()

#SHOPS
@st.cache_data(ttl=600,show_spinner = False)
def get_data():
    db = client.mydb
    items = db.all_flatten.find({},{"_id":1, "shop_url" : 1})
    items = list(items)
    return items

@st.cache_data(ttl=600,show_spinner = False)
def get_data_no_flatten() :
    db = client.mydb
    items = db.mycollection.find({"completeness" : {"$exists" : True}},{"_id":0, "completeness":1, "shop_url" : 1})
    items = list(items)
    return items

items = get_data()
items_noflatten = get_data_no_flatten()

count_dict_url = {}
count_dict_complete = {}

for key in items :
    if key["shop_url"] not in count_dict_url :
        count_dict_url[key["shop_url"]] = 1
    else:
        count_dict_url[key["shop_url"]] += 1

for key in items_noflatten :
    if key["shop_url"] not in count_dict_complete :
        count_dict_complete[key["shop_url"]] = key["completeness"]
    else:
        count_dict_complete[key["shop_url"]] += key["completeness"]

#print(count_dict_complete)

url_list = list(count_dict_url)
complete_list = list(count_dict_complete)

shopsName = []
produkteAnzahl = []
completenessAnzahl = []

for item in range(len(url_list)) : 
    shopsName.append(url_list[item])
    produkteAnzahl.append(count_dict_url[url_list[item]])
    average = count_dict_complete[url_list[item]]/count_dict_url[complete_list[item]]
    completenessAnzahl.append(round(average,2))

completeShop = []

#print(completenessAnzahl)

count = 0
choice = " keinem "

st.subheader("Durschnittliche Completeness")

#Completeness DURCHSCHNITT

for i in range(len(produkteAnzahl)) :
    count = count + produkteAnzahl[i] 

# --- TABELLE ---

dt = pd.DataFrame({
    "shopname" : shopsName ,
    "completeness" : completenessAnzahl
})

st.dataframe(dt,
            column_config={
                "shopname":"Shop",
                "completeness" : "Completeness"
            }, 
            hide_index = True,)