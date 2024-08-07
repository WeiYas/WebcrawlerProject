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
st.markdown('<style>h1{font-size:25px;} h3{font-size:20px;}</style>', unsafe_allow_html=True)

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

checkArr = [checkEdeka,checkVekoop,checkSuper,checkVolg,checkGlobus,checkHeine,checkLidl,checkMega,checkRewe]

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
   st.write("Wähle links zwei Shops aus um die miteinander zu vergleichen")

   countTrue = 0
   for i in range(len(checkArr)) :
      if checkArr[i] == True :
         countTrue += 1
   
   if countTrue == 2:

      #Edeka im Vergleich mit anderen Shops
      if checkEdeka == True and checkVekoop == True:
         choice = "Edeka und Vekoop"
         chart_data = pd.DataFrame({'name': ["Edeka","Vekoop"],'number of products':[countE,countV]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countE+countV , ' Produkte im ',choice,' Onlineshop')

      #iterations if Vekoop checked
      if checkEdeka == True and checkGlobus:
         choice = "Edeka und Globus"
         chart_data = pd.DataFrame({'name': ["Edeka","Globus"],'number of products':[countE,countG]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countE + countG , ' Produkte im ',choice,' Onlineshop')

      if checkEdeka == True and checkHeine == True:
         choice = "Edeka und Heinemann"
         chart_data = pd.DataFrame({'name': ["Edeka","Heinemann"],'number of products':[countE, countH]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countE + countH , ' Produkte im ',choice,' Onlineshop')
      
      if checkEdeka == True and checkLidl == True:
         choice = "Edeka und Lidl"
         chart_data = pd.DataFrame({'name': ["Edeka","Lidl"],'number of products':[countE,countL]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countE+countL , ' Produkte im ',choice,' Onlineshop')

      if checkEdeka == True and checkRewe == True:
         choice = "Edeka und Rewe"
         chart_data = pd.DataFrame({'name': ["Edkea","Rewe"],'number of products':[countE,countR]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countE + countR , ' Produkte im ',choice,' Onlineshop')

      if checkEdeka == True and checkSuper == True:
         choice = "Edeka und Supermarkt24h"
         chart_data = pd.DataFrame({'name': ["Edeka","Supermarkt24h"],'number of products':[countE,countS]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countE + countS , ' Produkte im ',choice,' Onlineshop')

      if checkEdeka == True and checkVolg == True:
         choice = "Edeka und Volg"
         chart_data = pd.DataFrame({'name': ["Edeka","Volg"],'number of products':[countE,countVo]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countE+countVo , ' Produkte im ',choice,' Onlineshop')

      if checkEdeka == True and checkMega == True:
         choice = "Heinemann"
         chart_data = pd.DataFrame({'name': ["Edeka","Mega Einkaufsparadies"],'number of products':[countE,countM]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countE + countM , ' Produkte im ',choice,' Onlineshop')
      
      if checkVekoop == True and checkGlobus:
         choice = "Vekoop und Globus"
         chart_data = pd.DataFrame({'name': ["Vekoop","Globus"],'number of products':[countV,countG]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countV + countG , ' Produkte im ',choice,' Onlineshop')

      if checkVekoop == True and checkHeine == True:
         choice = "Vekoop und Heinemann"
         chart_data = pd.DataFrame({'name': ["Vekoop","Heinemann"],'number of products':[countV, countH]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countV + countH , ' Produkte im ',choice,' Onlineshop')
      
      if checkVekoop == True and checkLidl == True:
         choice = "Vekoop und Lidl"
         chart_data = pd.DataFrame({'name': ["Vekoop","Lidl"],'number of products':[countV,countL]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countV+countL , ' Produkte im ',choice,' Onlineshop')

      if checkVekoop == True and checkRewe == True:
         choice = "Vekoop und Rewe"
         chart_data = pd.DataFrame({'name': ["Vekoop","Rewe"],'number of products':[countV,countR]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countV + countR , ' Produkte im ',choice,' Onlineshop')

      if checkVekoop == True and checkSuper == True:
         choice = "Vekoop und Supermarkt24h"
         chart_data = pd.DataFrame({'name': ["Vekoop","Supermarkt24h"],'number of products':[countV,countS]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countV + countS , ' Produkte im ',choice,' Onlineshop')

      if checkVekoop == True and checkVolg == True:
         choice = "Vekoop und Volg"
         chart_data = pd.DataFrame({'name': ["Vekoop","Volg"],'number of products':[countV,countVo]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countV+countVo , ' Produkte im ',choice,' Onlineshop')

      if checkVekoop == True and checkMega == True:
         choice = "Vekoop und Mega Einkaufsparadies"
         chart_data = pd.DataFrame({'name': ["Vekoop","Mega Einkaufsparadies"],'number of products':[countV,countM]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countV + countM , ' Produkte im ',choice,' Onlineshop')

      if checkGlobus == True and checkHeine == True:
         choice = "Globus und Heinemann"
         chart_data = pd.DataFrame({'name': ["Globus","Heinemann"],'number of products':[countG, countH]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countG + countH , ' Produkte im ',choice,' Onlineshop')
      
      if checkGlobus == True and checkLidl == True:
         choice = "Globus und Lidl"
         chart_data = pd.DataFrame({'name': ["Globus","Lidl"],'number of products':[countG,countL]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countG+countL , ' Produkte im ',choice,' Onlineshop')

      if checkGlobus == True and checkRewe == True:
         choice = "Globus und Rewe"
         chart_data = pd.DataFrame({'name': ["Globus","Rewe"],'number of products':[countG,countR]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countG + countR , ' Produkte im ',choice,' Onlineshop')

      if checkGlobus == True and checkSuper == True:
         choice = "Globus und Supermarkt24h"
         chart_data = pd.DataFrame({'name': ["Globus","Supermarkt24h"],'number of products':[countG,countS]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countG + countS , ' Produkte im ',choice,' Onlineshop')

      if checkGlobus == True and checkVolg == True:
         choice = "Globus und Volg"
         chart_data = pd.DataFrame({'name': ["Globus","Volg"],'number of products':[countG,countVo]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countG+countVo , ' Produkte im ',choice,' Onlineshop')

      if checkGlobus == True and checkMega == True:
         choice = "Globus und Mega Einkaufsparadies"
         chart_data = pd.DataFrame({'name': ["Globus","Mega Einkaufsparadies"],'number of products':[countG,countM]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countG + countM , ' Produkte im ',choice,' Onlineshop')

      if checkHeine == True and checkLidl == True:
         choice = "Heinemann und Lidl"
         chart_data = pd.DataFrame({'name': ["Heinemann","Lidl"],'number of products':[countH,countL]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countH+countL , ' Produkte im ',choice,' Onlineshop')

      if checkHeine == True and checkRewe == True:
         choice = "Heinemann und Rewe"
         chart_data = pd.DataFrame({'name': ["Heinemann","Rewe"],'number of products':[countH,countR]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countH + countR , ' Produkte im ',choice,' Onlineshop')

      if checkHeine == True and checkSuper == True:
         choice = "Heinemann und Supermarkt24h"
         chart_data = pd.DataFrame({'name': ["Heinemann","Supermarkt24h"],'number of products':[countH,countS]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countH + countS , ' Produkte im ',choice,' Onlineshop')

      if checkHeine == True and checkVolg == True:
         choice = "Heinemann und Volg"
         chart_data = pd.DataFrame({'name': ["Heinemann","Volg"],'number of products':[countH,countVo]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countH+countVo , ' Produkte im ',choice,' Onlineshop')

      if checkHeine == True and checkMega == True:
         choice = "Heinemann und Mega Einkaufsparadies"
         chart_data = pd.DataFrame({'name': ["Heinemann","Mega Einkaufsparadies"],'number of products':[countH,countM]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countH + countM , ' Produkte im ',choice,' Onlineshop')
      
      if checkLidl == True and checkRewe == True:
         choice = "Lidl und Rewe"
         chart_data = pd.DataFrame({'name': ["Lidl","Rewe"],'number of products':[countL,countR]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countL + countR , ' Produkte im ',choice,' Onlineshop')

      if checkLidl  == True and checkSuper == True:
         choice = "Lidl und Supermarkt24h"
         chart_data = pd.DataFrame({'name': ["Lidl","Supermarkt24h"],'number of products':[countL,countS]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countL + countS , ' Produkte im ',choice,' Onlineshop')

      if checkLidl  == True and checkVolg == True:
         choice = "Lidl und Volg"
         chart_data = pd.DataFrame({'name': ["Lidl","Volg"],'number of products':[countL,countVo]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countL+countVo , ' Produkte im ',choice,' Onlineshop')

      if checkLidl == True and checkMega == True:
         choice = "Lidl und Mega Einkaufsparadies"
         chart_data = pd.DataFrame({'name': ["Lidl","Mega Einkaufsparadies"],'number of products':[countL,countM]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countL + countM , ' Produkte im ',choice,' Onlineshop')

      if checkRewe  == True and checkSuper == True:
         choice = "Rewe und Supermarkt24h"
         chart_data = pd.DataFrame({'name': ["Rewe","Supermarkt24h"],'number of products':[countR,countS]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countR + countS , ' Produkte im ',choice,' Onlineshop')

      if checkRewe  == True and checkVolg == True:
         choice = "Rewe und Volg"
         chart_data = pd.DataFrame({'name': ["Rewe","Volg"],'number of products':[countR,countVo]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countR+countVo , ' Produkte im ',choice,' Onlineshop')

      if checkRewe == True and checkMega == True:
         choice = "Rewe und Mega Einkaufsparadies"
         chart_data = pd.DataFrame({'name': ["Rewe","Mega Einkaufsparadies"],'number of products':[countR,countM]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countR + countM , ' Produkte im ',choice,' Onlineshop')

      if checkSuper  == True and checkVolg == True:
         choice = "Supermarkt24h und Volg"
         chart_data = pd.DataFrame({'name': ["Supermarkt24h","Volg"],'number of products':[countS,countVo]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countS+countVo , ' Produkte im ',choice,' Onlineshop')

      if checkSuper == True and checkMega == True:
         choice = "Supermarkt24h und Mega Einkaufsparadies"
         chart_data = pd.DataFrame({'name': ["Supermarkt24h","Mega Einkaufsparadies"],'number of products':[countS,countM]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countS + countM , ' Produkte im ',choice,' Onlineshop')

      if checkVolg == True and checkMega == True:
         choice = "Volg und Mega Einkaufsparadies"
         chart_data = pd.DataFrame({'name': ["Volg","Mega Einkaufsparadies"],'number of products':[countVo,countM]})
         chart_data = chart_data.set_index('name')
         st.bar_chart(chart_data)
         st.write(countVo + countM , ' Produkte im ',choice,' Onlineshop')



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


