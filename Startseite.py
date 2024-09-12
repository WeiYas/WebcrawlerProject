import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(
    layout="wide",
    page_title="Startseite",
    page_icon="random"
)
st.markdown('<style>h1{font-size:25px;} h3{font-size:20px;}', unsafe_allow_html=True)

# footer test .footer {position: fixed;left: 0;bottom: 0;width: 100%;background-color: red;color: white;text-align: center;}</style> <div class="footer"> <p>Footer</p> </div>'

# https://www.volgshop.ch/ , https://shop.rewe.de/ , "https://www.lidl.de/" , "https://www.supermarkt24h.de/" , "https://www.heinemann-shop.com/", "https://www.mega-einkaufsparadies.de/"

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()

col1, col2 = st.columns(2)

with col1:
    st.title("Webcrawler Dashboard")
with col2:
    st.image('logo_ucb.png',width = 500)



st.markdown('<style> .footer{position: fixed;left: 0;bottom: 0;width: 100%;color: black;text-align: center;}</style> <div class="footer"><p>Umwelt-Campus Birkenfeld</p></div>',unsafe_allow_html=True)

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


#print(produkteAnzahl)

count = 0
choice = " keinem "

st.subheader("Anzahl der Shops und Produkte")

#Completeness DURCHSCHNITT

for i in range(len(produkteAnzahl)) :
    count = count + produkteAnzahl[i] 

# --- TABELLE ---

df = pd.DataFrame([
    [str(len(shopsName)), count]], 
    columns = ["Anzahl Shops" , "Anzahl Produkte"]
)
#df = pd.DataFrame(np.random.randn(10, 5), columns=["cols"])

dt = pd.DataFrame({
    "shopname" : shopsName ,
    "produkteAnzahl" :  produkteAnzahl,
    "completeness" : completenessAnzahl
})

#st.write("- Anzahl Shops:" , str(len(shopsName)))
#st.write("- Anzahl aller Produkte: ", str(count))

st.dataframe(df,
            column_config={
                "anzahlShops":"Shop",
                "produkteAnzahl" : "Anzahl aller Produkte",
            }, 
            hide_index = True,)

st.dataframe(dt,
            column_config={
                "shopname":"Shop",
                "produkteAnzahl" : "Anzahl Produkte",
                "completeness" : "Completeness"
            }, 
            hide_index = True,)

    