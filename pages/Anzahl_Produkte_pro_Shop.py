import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np

st.title("Anzahl Produkte pro Shop")
st.write("Wähle links einen oder mehrere Shops aus um deren Anzahl an Produkten anzuzeigen")

col1, col2 = st.columns(2)

checkEdeka = st.sidebar.checkbox("Edeka")
checkVekoop = st.sidebar.checkbox("Vekoop")

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()

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

countE = 0
countV = 0
count = 0
choice = " keinem "

#iterations if Edeka checked
if checkEdeka == True:
   with col1:
      itemsEdeka = get_data_Edeka()
      for i in itemsEdeka:
         countE += 1
      count = countE
      choice = "Edeka"
      chart_data = pd.DataFrame({'name': ["Edeka"],'number of products':[countE]})
      st.bar_chart(chart_data)

#iterations if Vekoop checked
if checkVekoop == True:
   with col2:
      itemsVekoop = get_data_Vekoop()
      for i in itemsVekoop:
         countV += 1
      count = countV
      choice = "Vekoop"
      chart_data = pd.DataFrame({'name': ["Vekoop"],'number of products':[countV]})
      st.bar_chart(chart_data)
   

if (checkEdeka == True and checkVekoop == True):
   count = countV + countE
   choice = "Edeka + Vekoop"
   chart_data = pd.DataFrame({
  'name': ["Edeka","Vekoop"],
  'number of products':[countE,countV]
   })

   chart_data = chart_data.set_index('name')
   st.bar_chart(chart_data)

st.write(count , ' Produkte im ',choice,' Onlineshop')


