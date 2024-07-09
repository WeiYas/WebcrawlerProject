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

options = st.multiselect(
    "Wähle Geschäfte und zeige welche Produkte in diesen gleichzeitig zur Verfügung stehen",
    ["Edeka", "Vekoop","Globus", "Supermarkt24h"])
st.write("Nur Produkte mit registriertem GTIN können angezeigt werden")
#st.write(len(options))

@st.cache_data(ttl=600)
def get_data():
    db = client.mydb
    items = db.all_flatten.find({'$expr': { '$getField': 'product_data/gtin' }}, {"product_data/gtin" : 1, "product_data/name" : 1 , "shop_url" : 1})
    items = list(items)
    return items

items = get_data()

# mehr als 2 shops

if len(options) == 2 :
    with st.spinner('Daten werden geladen...'):

        numShop = len(options)
        urls = ["https://www.edeka24.de/","https://www.vekoop.de/", "https://www.globus.de/", "https://www.supermarkt24h.de/"]

        arrE,arrV,arrG, arrS = [],[],[],[]       
        arrSameE,arrSameV,arrSameG,arrSameS = [], [],[],[]
        name0, name1 = [] , []
        lenG = 0

        for i in range(numShop):
            for item in items :
                if item["shop_url"] == "https://www.edeka24.de/" and options[i] == "Edeka" :
                    arrE.append(item["product_data/gtin"])
                elif item["shop_url"] == "https://www.vekoop.de/" and options[i] == "Vekoop" :
                    arrV.append(item["product_data/gtin"])
                elif item["shop_url"] == "https://www.globus.de/" and options[i] == "Globus" :
                    arrG.append(item["product_data/gtin"])
                elif item["shop_url"] == "https://www.supermarkt24h.de/" and options[i] == "Supermarkt24h" :
                    arrS.append(item["product_data/gtin"])
                

        if (options[0] == "Edeka" and options[1]=="Vekoop") or (options[1] == "Edeka" and options[0]=="Vekoop") :
            for a in range(len(arrE)):
                for b in range(len(arrV)) :
                    if arrE[a] == arrV[b] :
                        arrSameE.append(arrE[a])
                        arrSameV.append(arrV[b])
        elif (options[0] == "Edeka" and options[1]=="Globus") or (options[1] == "Edeka" and options[0]=="Globus") :
            for a in range(len(arrE)):
                for b in range(len(arrG)) :
                    if arrE[a] == arrG[b] :
                        arrSameE.append(arrE[a])
                        arrSameG.append(arrG[b])
        elif (options[0] == "Vekoop" and options[1]=="Globus") or (options[0] == "Globus" and options[1]=="Vekoop") :
            for a in range(len(arrV)):
                for b in range(len(arrG)) :
                    if arrV[a] == arrG[b] :
                        arrSameV.append(arrV[a])
                        arrSameG.append(arrG[b])
        elif (options[0] == "Supermarkt24h" and options[1]=="Globus") or (options[0] == "Globus" and options[1]=="Supermarkt24h") :
            for a in range(len(arrS)):
                for b in range(len(arrG)) :
                    if arrS[a] == arrG[b] :
                        arrSameS.append(arrS[a])
                        arrSameG.append(arrG[b])
        elif (options[0] == "Supermarkt24h" and options[1]=="Edeka") or (options[0] == "Edeka" and options[1]=="Supermarkt24h") :
            for a in range(len(arrS)):
                for b in range(len(arrE)) :
                    if arrS[a] == arrE[b] :
                        arrSameS.append(arrS[a])
                        arrSameE.append(arrE[b])

            for i in range(len(arrSameS)) :    
                for item in items: 
                    if item["product_data/gtin"] == arrSameS[i] and item["shop_url"] == "https://www.supermarkt24h.de/":
                        name0.append(item["product_data/name"])
                    if item["product_data/gtin"] == arrSameE[i] and item["shop_url"] == "https://www.edeka24.de/":
                        name1.append(item["product_data/name"])
            lenG = len(arrSameS)
            print(len(arrSameS))
            print(len(name0))
            print(len(name1))
       
        st.subheader("Diese Produkte gibt es in beiden Geschäften")
        #print(arrSameE)
        #print(arrSameG)
        
        st.write("Anzahl gleicher Produkte: " ,str(lenG))




            



