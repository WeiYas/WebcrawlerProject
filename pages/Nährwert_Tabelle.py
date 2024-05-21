import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

onOverall = st.sidebar.toggle("Nährwert Vorhanden",value=True)
onAttribute = st.sidebar.toggle("Attribute ausgefüllt")
onSingle = st.sidebar.toggle("Nährwerte pro Produkt")

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()

@st.cache_data(ttl=600)
def get_data_tableJa():
    db = client.mydb
    items = db.mycollection.find({"product_data.nutrition_table":{"$exists":"true"}} , {"_id": 1})
    items = list(items)
    return items

@st.cache_data(ttl=600)
def get_data():
    db = client.mydb
    items = db.mycollection.find({},{"_id": 1})
    items = list(items)
    return items

tableJa = get_data_tableJa()
tableAll = get_data()
count = 0
countJa = 0
countNe = 0

for i in tableJa :
    countJa += 1

for i in tableAll : 
    count += 1

countNe = count - countJa

#Attribute Anzeigen rechnen


#Anzeige Browser

if onOverall:
    st.title("Nährwerttabelle existiert")
    chart_data = pd.DataFrame({
    'Nährwert Tabelle vorhanden': ["ja","nein"],
    'Anzahl Produkte':[countJa,countNe]
    })
    c = ( 
        alt.Chart(chart_data).mark_bar().encode(x='Nährwert Tabelle vorhanden',y='Anzahl Produkte')
        )
    st.altair_chart(c, use_container_width=True)

if onAttribute:
    
    st.title("Durchschnittliche Nährwerte aller Produkte")

    @st.cache_data(ttl=600)
    def get_data_cal():
        db = client.mydb
        items = db.mycollection.find({"product_data.nutrition_table.calories":{"$exists":"true"}},{"_id": 0, "product_data" :{ "nutrition_table" : 1} })
        items = list(items)
        return items

    calItem = get_data_cal()

    countCal = 0
    for item in calItem:
        countCal += 1
    st.write("- Kalorien gespeichert bei :" , countCal , "Produkten")

    @st.cache_data(ttl=600)
    def get_data_carbo():
        db = client.mydb
        items = db.mycollection.find({"product_data.nutrition_table.carbohydrate_content":{"$exists":"true"}},{"_id": 0, "product_data" :{ "nutrition_table" : 1} })
        items = list(items)
        return items

    carbItem = get_data_carbo()

    countCarb = 0
    for item in carbItem:
        countCarb += 1
    st.write("- Products with carbohydrate_content shown:" , countCarb)

    @st.cache_data(ttl=600)
    def get_data_fat():
        db = client.mydb
        items = db.mycollection.find({"product_data.nutrition_table.fat_content":{"$exists":"true"}},{"_id": 0, "product_data" :{ "nutrition_table" : 1} })
        items = list(items)
        return items

    fatItem = get_data_fat()

    countfat = 0
    for item in fatItem:
        countfat += 1
    st.write("- Products with fat_content shown:" , countfat)

    @st.cache_data(ttl=600)
    def get_data_fib():
        db = client.mydb
        items = db.mycollection.find({"product_data.nutrition_table.fiber_content":{"$exists":"true"}},{"_id": 0, "product_data" :{ "nutrition_table" : 1} })
        items = list(items)
        return items

    fibItem = get_data_fib()

    countfib = 0
    for item in fibItem:
        countfib += 1
    st.write("- Products with fiber_content shown:" , countfib)

    @st.cache_data(ttl=600)
    def get_data_prot():
        db = client.mydb
        items = db.mycollection.find({"product_data.nutrition_table.protein_content":{"$exists":"true"}},{"_id": 0, "product_data" :{ "nutrition_table" : 1} })
        items = list(items)
        return items

    protItem = get_data_prot()

    countprot = 0
    for item in protItem:
        countprot += 1
    st.write("- Products with protein_content shown:" , countfib)

    diaOn = st.toggle("Show Diagramm")

    if diaOn : 
        chart_data = pd.DataFrame({
            'Nährwerte': ["Kalorien","Carbonhydrate", "Fette" , "Fiber", "Proteine"],
            'Anzahl Produkte':[countCal,countCarb,countfat,countfib,countprot]            })
        c = ( 
            alt.Chart(chart_data).mark_bar().encode(x='Nährwerte',y='Anzahl Produkte')
        )
        st.altair_chart(c, use_container_width=True)

if onSingle :
    st.title("Nährwerte eines ausgewählten Produkt")

    @st.cache_data(ttl=600)
    def get_data():
        db = client.mydb
        items = db.mycollection.find({"product_data.nutrition_table":{"$exists":"true"}},{"_id": 0,  "shop_url" : 1 , "product_data" :{ "name" : 1} })
        items = list(items)
        return items
    
    allItems = get_data()

    @st.cache_data(ttl=600)
    def get_data_cal():
        db = client.mydb
        items = db.mycollection.find({"product_data.nutrition_table.calories":{"$exists":"true"}},{"_id": 0, "product_data" :{ "nutrition_table" : 1, "name" : 1} })
        items = list(items)
        return items

    calItem = get_data_cal()

    @st.cache_data(ttl=600)
    def get_data_carbo():
        db = client.mydb
        items = db.mycollection.find({"product_data.nutrition_table.carbohydrate_content":{"$exists":"true"}},{"_id": 0, "product_data" :{ "nutrition_table" : 1 , "name" : 1} })
        items = list(items)
        return items

    carbItem = get_data_carbo()

    @st.cache_data(ttl=600)
    def get_data_fat():
        db = client.mydb
        items = db.mycollection.find({"product_data.nutrition_table.fat_content":{"$exists":"true"}},{"_id": 0, "product_data" :{ "nutrition_table" : 1, "name" : 1} })
        items = list(items)
        return items

    fatItem = get_data_fat()

    @st.cache_data(ttl=600)
    def get_data_fib():
        db = client.mydb
        items = db.mycollection.find({"product_data.nutrition_table.fiber_content":{"$exists":True}},{"_id": 0, "product_data" :{ "nutrition_table" : 1, "name" : 1} })
        items = list(items)
        return items

    fibItem = get_data_fib()

    @st.cache_data(ttl=600)
    def get_data_nofib():
        db = client.mydb
        items = db.mycollection.find({"product_data.nutrition_table.fiber_content":{"$exists":False}},{"_id": 0, "product_data" :{ "nutrition_table" : 1, "name" : 1} })
        items = list(items)
        return items

    nofibItem = get_data_nofib()

    countF = 0

    for i in fibItem: 
        countF += 1

    st.title(countF)

    @st.cache_data(ttl=600)
    def get_data_prot():
        db = client.mydb
        items = db.mycollection.find({"product_data.nutrition_table.protein_content":{"$exists":"true"}},{"_id": 0, "product_data" :{ "nutrition_table" : 1, "name" : 1} })
        items = list(items)
        return items

    protItem = get_data_prot()

    @st.cache_data(ttl=600)
    def get_data_satf():
        db = client.mydb
        items = db.mycollection.find({"product_data.nutrition_table.saturated_fat_content":{"$exists":"true"}},{"_id": 0, "product_data" :{ "nutrition_table" : 1, "name" : 1} })
        items = list(items)
        return items

    satfItem = get_data_satf()

    #Anzeigen Nährstoffe eines Produktes

    title = st.text_input("Produkt auswählen", "Holle frucht pur Pouchy Birne & Aprikose - Bio - 90g - vekoop.de")
    st.write("Das ausgewählte Produkt ist: ", title)

    for i in allItems : 
        if i["product_data"]["name"] == title and i["shop_url"] == "https://www.edeka24.de/" :
            st.write("Genau dieses Produkt gibt es im Edeka")
        elif i["product_data"]["name"] == title and i["shop_url"] == "https://www.vekoop.de/" :
            st.write("Genau dieses Produkt gibt es im Vekoop")

    left, right = st.columns(2)

    with left: 
        # Kalorien Anzeige
        for i in calItem : 
            if i["product_data"]["name"] == title and i["product_data"]["nutrition_table"]["calories"]:
                st.subheader("Kalorien")
                st.write("Kalorien in kJ: " , str(i["product_data"]["nutrition_table"]["calories"][0]["value"]))
                st.write("Kalorien in kcal: " , str(i["product_data"]["nutrition_table"]["calories"][1]["value"]))
        
        # Carbohydrates Anzeige
        for i in carbItem:
            if i["product_data"]["name"] == title and i["product_data"]["nutrition_table"]["carbohydrate_content"]:
                st.subheader("Kohlenhydrate")
                st.write("Anzahl der Kohlenhydrate: " , str(i["product_data"]["nutrition_table"]["carbohydrate_content"]["value"]), " in ", i["product_data"]["nutrition_table"]["carbohydrate_content"]["unit"] )
        
        for i in fatItem:
            if i["product_data"]["name"] == title and i["product_data"]["nutrition_table"]["fat_content"]:
                st.subheader("Fettgehalt")
                st.write("Anzahl der Fette: " , str(i["product_data"]["nutrition_table"]["fat_content"]["value"]), " in ", i["product_data"]["nutrition_table"]["fat_content"]["unit"] )
        
        for i in range(len(fibItem)):
            if fibItem[i]["product_data"]["name"] == title and fibItem[i]["product_data"]["nutrition_table"]["fiber_content"]:
                st.subheader("Ballaststoffgehalt")
                st.write("Anzahl der Fette: " , str(fibItem[i]["product_data"]["nutrition_table"]["fiber_content"]["value"]), " in ", fibItem[i]["product_data"]["nutrition_table"]["fiber_content"]["unit"] )
    

    with right : 
        for i in protItem : 
            if i["product_data"]["name"] == title and i["product_data"]["nutrition_table"]["protein_content"]:
                st.subheader("Proteine")
                st.write("Anzahl der Proteine: " , str(i["product_data"]["nutrition_table"]["protein_content"]["value"]), " in ", i["product_data"]["nutrition_table"]["protein_content"]["unit"] )

        for i in satfItem : 
            if i["product_data"]["name"] == title and i["product_data"]["nutrition_table"]["saturated_fat_content"]:
                st.subheader("Gesättigte Fettsäuren")
                st.write("Anzahl der gesättigten Fettsäuren: " , str(i["product_data"]["nutrition_table"]["saturated_fat_content"]["value"]), " in ", i["product_data"]["nutrition_table"]["saturated_fat_content"]["unit"] )
    
        