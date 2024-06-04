import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np


# https://www.volgshop.ch/ , https://shop.rewe.de/ , "https://www.lidl.de/" , "https://www.supermarkt24h.de/" , "https://www.heinemann-shop.com/", "https://www.mega-einkaufsparadies.de/"

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()

st.title("Anzahl Produkte pro Shop")
st.write("Wähle links einen oder mehrere Shops aus um deren Anzahl an Produkten anzuzeigen")

tabOne , tabAll = st.tabs(["Einzelansicht","Gesamtsicht"])

checkEdeka = st.sidebar.checkbox("Edeka")
checkVekoop = st.sidebar.checkbox("Vekoop")
checkGlobus = st.sidebar.checkbox("Globus")
checkVolg = st.sidebar.checkbox("Volg")
checkRewe = st.sidebar.checkbox("Rewe")
checkLidl = st.sidebar.checkbox("Lidl")
checkSuper = st.sidebar.checkbox("Supermarkt24h")
checkHeine = st.sidebar.checkbox("Heinemann")
checkMega = st.sidebar.checkbox("Mega Einkaufsparadies")

@st.cache_data(ttl=600)
def get_data_Edeka():
    db = client.mydb
    items = db.mycollection.find({"shop_url":"https://www.edeka24.de/"},{"_id":1})
    items = list(items)
    return items

#nur ID abfragen evt

@st.cache_data(ttl=600)
def get_data_Vekoop():
    db = client.mydb
    items = db.mycollection.find({"shop_url":"https://www.vekoop.de/"},{"_id":1})
    items = list(items)
    return items

@st.cache_data(ttl=600)
def get_data_Globus():
    db = client.mydb
    items = db.mycollection.find({"shop_url" : "https://www.globus.de/"},{"_id":1})
    items = list(items)
    return items

@st.cache_data(ttl=600)
def get_data_Volg():
    db = client.mydb
    items = db.mycollection.find({"shop_url" : "https://www.volgshop.ch/"},{"_id":1})
    items = list(items)
    return items

@st.cache_data(ttl=600)
def get_data_Rewe():
    db = client.mydb
    items = db.mycollection.find({"shop_url" : "https://shop.rewe.de/"},{"_id":1})
    items = list(items)
    return items

@st.cache_data(ttl=600)
def get_data_Lidl():
    db = client.mydb
    items = db.mycollection.find({"shop_url" : "https://www.lidl.de/"},{"_id":1})
    items = list(items)
    return items

@st.cache_data(ttl=600)
def get_data_Super():
    db = client.mydb
    items = db.mycollection.find({"shop_url" : "https://www.supermarkt24h.de/"},{"_id":1})
    items = list(items)
    return items

@st.cache_data(ttl=600)
def get_data_Mega():
    db = client.mydb
    items = db.mycollection.find({"shop_url" : "https://www.mega-einkaufsparadies.de/"},{"_id":1})
    items = list(items)
    return items

@st.cache_data(ttl=600)
def get_data_Heine():
    db = client.mydb
    items = db.mycollection.find({"shop_url" : "https://www.heinemann-shop.com/"},{"_id":1})
    items = list(items)
    return items


count = 0
countE = 0
countV = 0
countG = 0
countVo = 0
countR = 0
countL = 0
countS = 0
countH = 0
countM = 0
choice = " keinem "

#Produkte zählen

itemsEdeka = get_data_Edeka()
for i in itemsEdeka:
   countE += 1
   count = countE

itemsVekoop = get_data_Vekoop()
for i in itemsVekoop:
   countV += 1
   count = countV

itemsGlobus = get_data_Globus()
for i in itemsGlobus:
   countG += 1
   count = countG

itemsVolg= get_data_Volg()
for i in itemsVolg:
   countVo += 1
   count = countVo

itemsRewe = get_data_Rewe()
for i in itemsRewe:
   countR += 1
   count = countR

itemsLidl = get_data_Lidl()
for i in itemsLidl:
   countL += 1
   count = countL

itemsSuper = get_data_Super()
for i in itemsSuper:
   countS += 1
   count = countS

itemsHeine = get_data_Heine()
for i in itemsHeine:
   countH += 1
   count = countH

itemsMega = get_data_Mega()
for i in itemsMega:
   countM += 1
   count = countM


#Einzelansicht
with tabOne :
   #iterations if Edeka checked
   col1, col2, col3, col4, col5, col6, col7,col8, col9 = st.columns(9)

   
   if checkEdeka == True:
      choice = "Edeka"
      with col1:
         chart_data = pd.DataFrame({'name': ["Edeka"],'number of products':[countE]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countE , ' Produkte im ',choice,' Onlineshop')

   #iterations if Vekoop checked
   if checkVekoop == True:
      choice = "Vekoop"
      with col2:
         chart_data = pd.DataFrame({'name': ["Vekoop"],'number of products':[countV]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countV , ' Produkte im ',choice,' Onlineshop')

   if checkGlobus == True:
      choice = "Globus"
      with col3:
         chart_data = pd.DataFrame({'name': ["Globus"],'number of products':[countG]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countV , ' Produkte im ',choice,' Onlineshop')
   
   if checkVolg == True:
      choice = "Volg"
      with col4:
         chart_data = pd.DataFrame({'name': ["Volg"],'number of products':[countVo]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countVo , ' Produkte im ',choice,' Onlineshop')

   if checkRewe == True:
      choice = "Rewe"
      with col5:
         chart_data = pd.DataFrame({'name': ["Rewe"],'number of products':[countR]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countR , ' Produkte im ',choice,' Onlineshop')

   if checkLidl == True:
      choice = "Lidl"
      with col6:
         chart_data = pd.DataFrame({'name': ["Lidl"],'number of products':[countL]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countL , ' Produkte im ',choice,' Onlineshop')

   if checkSuper == True:
      choice = "Supermarkt24h"
      with col7:
         chart_data = pd.DataFrame({'name': ["Supermarkt24h"],'number of products':[countS]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countS , ' Produkte im ',choice,' Onlineshop')

   if checkHeine == True:
      choice = "Heinemann"
      with col8:
         chart_data = pd.DataFrame({'name': ["Heinemann"],'number of products':[countH]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countH , ' Produkte im ',choice,' Onlineshop')

   if checkMega == True:
      choice = "Mega Einkaufsparadies"
      with col9:
         chart_data = pd.DataFrame({'name': ["Mega Einkaufsparadies"],'number of products':[countM]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countM , ' Produkte im ',choice,' Onlineshop')

#Gesamtansicht
with tabAll :
      count = countV + countE + countG + countVo + countR + countL + countS + countH + countM
      chart_data = pd.DataFrame({
      'name': ["Edeka","Vekoop", "Globus" , "Volg", "Rewe", "Lidl", "Supermarkt24h" , "Heinemann", "Mega Einkaufsparadies"],
      'number of products':[countE,countV, countG, countVo, countR, countL, countS, countH, countM]
         })

      chart_data = chart_data.set_index('name')
      st.bar_chart(chart_data)
      st.write(count , ' Produkte in allen Onlineshops')


