import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import time

DB = st.secrets["mongo"]["db"]
COL = st.secrets["mongo"]["col"]

choice = st.sidebar.radio(
    "Auswahl zum Anzeigen",
    ["Produkte vorhanden", "Nährwerte Produkte", "Nährwert ein Produkt"])

@st.cache_resource
def init_connection():
    connection_string = "mongodb://localhost:27017/"
    return pymongo.MongoClient(connection_string)

client = init_connection()

@st.cache_data(ttl=600)
def get_data():
    db = client[DB]
    items = db[COL].find({"product_data.nutrition_table": {"$exists": True}},{"_id": 0,  "shop_url" : 1 , "product_data" :{ "nutrition_table" : 1 , "name" : 1} })
    items = list(items)
    return items
    
def get_len():
    db = client[DB]
    items = db[COL].find({},{"_id": 1})
    len_all = len(list(items))
    return len_all

start_time = time.time()
all_len = get_len()
tableAll = get_data()
allItems = get_data()
time_data = time.time() - start_time
#Attribute Anzeigen rechnen


#Anzeige Browser

if choice == "Produkte vorhanden":
    count = len
    countJa = len(tableAll)
    countNe = all_len - countJa

    st.title("Nährwerttabelle existiert")
    chart_data = pd.DataFrame({
    'Nährwert Tabelle vorhanden': ["ja","nein"],
    'Anzahl Produkte':[countJa,countNe]
    })
    c = ( 
        alt.Chart(chart_data).mark_bar().encode(x='Nährwert Tabelle vorhanden',y='Anzahl Produkte')
        )
    st.altair_chart(c, use_container_width=True)

    st.write(f"Zeit für Datenanfrage: {time_data}")

if choice == "Nährwerte Produkte":

    start_list = time.time()
    #get list where calories exist
    cal, carbo, fat, fiber, protItem, satfItem, sodItem, sugItem = [], [], [], [], [], [], [], []
    for item in allItems:
        try:
            cal.append(item["product_data"]["nutrition_table"]["calories"])
        except KeyError:
            pass
        try:
            carbo.append(item["product_data"]["nutrition_table"]["carbohydrate_content"])
        except KeyError:
            pass
        try:
            fat.append(item["product_data"]["nutrition_table"]["fat_content"])
        except KeyError:
            pass
        try:
            fiber.append(item["product_data"]["nutrition_table"]["fiber_content"])
        except KeyError:
            pass
        try:
            protItem.append(item["product_data"]["nutrition_table"]["cprotein_content"])
        except KeyError:
            pass
        try:
            satfItem.append(item["product_data"]["nutrition_table"]["saturated_fat_content"])
        except KeyError:
            pass
        try:
            sodItem.append(item["product_data"]["nutrition_table"]["sodium_content"])
        except KeyError:
            pass
        try:
            sugItem.append(item["product_data"]["nutrition_table"]["sugar_content"])
        except KeyError:
            pass
    
    list_time = time.time() - start_list

    st.title("Durchschnittliche Nährwerte aller Produkte")

    tabData, tabChart = st.tabs(["Data", "Diagram"])

    with tabData:

        colLeft, colRight = st.columns(2)

        with colLeft:

            countCal = len(cal)
            countCarb = len(carbo)
            countfat = len(fat)
            countfib = len(fiber)

            st.write("**Produkte mit Kalorien**" , str(countCal))
            st.write("**Produkte mit Kohlenhydraten**",str(countCarb))
            st.write("**Produkte mit Fetten**" , str(countfat))
            st.write("**Produkten mit Ballaststoffen**" , str(countfib))
        
        with colRight :

            countprot = len(protItem)
            
            countsf = len(satfItem)
            
            countsod = len(sodItem)
            
            countsug = len(sugItem)
            
            st.write("**Produkte mit Proteinen**" , str(countfib))
            st.write("**Produkte mit gesättigten Fettsäuren**" , str(countsf))
            st.write("**Produkte mit Natrium**" , str(countsod))
            st.write("**Produkte mit Zuckeranteil**" , str(countsug))
            

    with tabChart:

        chart_data = pd.DataFrame({
            'Nährwerte': ["Kalorien","Carbonhydrate", "Fette" , "Fiber", "Proteine", "Ges.Fettsäuren", "Natrium"],
            'Anzahl Produkte':[countCal,countCarb,countfat,countfib,countprot,countsf,countsod]})
        c = ( 
           alt.Chart(chart_data).mark_bar().encode(x='Nährwerte',y='Anzahl Produkte')
        )
        st.altair_chart(c, use_container_width=True)

    st.write(f"Zeit für Datenanfrage: {time_data}")
    st.write(f"Zeit für Zählschleife: {list_time}")

if choice == "Nährwert ein Produkt" :
    st.title("Nährwerte eines ausgewählten Produktes")

    #Anzeigen Nährstoffe eines Produktes

    title = st.text_input("Produktname eintippen", "Holle frucht pur Pouchy Birne & Aprikose - Bio - 90g - vekoop.de")
    
    container = st.container(border = True)

    with container:
        st.write(f"Das ausgewählte Produkt ist:&nbsp; **{title}**")
        for i in allItems : 
            if i["product_data"]["name"] == title and i["shop_url"] == "https://www.edeka24.de/" :
                st.write("Genau dieses Produkt gibt es im **Edeka**")
            elif i["product_data"]["name"] == title and i["shop_url"] == "https://www.vekoop.de/" :
                st.write("Genau dieses Produkt gibt es im **Vekoop**")

    searchItem = False

    for i in tableAll :
        if i["product_data"]["name"] == title :
            searchItem = True

            
    #st.write(searchItem)

    left, right = st.columns(2)

    if searchItem:
        with left: 
            # Kalorien Anzeige
            for i in tableAll: 
                if i["product_data"]["name"] == title and i["product_data"]["nutrition_table"]["calories"]:
                    st.subheader("Kalorien")
                    st.write("Kalorien in kJ: " , str(i["product_data"]["nutrition_table"]["calories"][0]["value"]))
                    st.write("Kalorien in kcal: " , str(i["product_data"]["nutrition_table"]["calories"][1]["value"]))
                if i["product_data"]["name"] == title and i["product_data"]["nutrition_table"]["carbohydrate_content"]:
                        st.subheader("Kohlenhydrate")
                        st.write("Anzahl der Kohlenhydrate: " , str(i["product_data"]["nutrition_table"]["carbohydrate_content"]["value"]), " in ", i["product_data"]["nutrition_table"]["carbohydrate_content"]["unit"] )
            # Carbohydrates Anzeige
               
            for i in fat:
                if i["product_data"]["name"] == title and i["product_data"]["nutrition_table"]["fat_content"]:
                    st.subheader("Fettgehalt")
                    st.write("Anzahl der Fette: " , str(i["product_data"]["nutrition_table"]["fat_content"]["value"]), " in ", i["product_data"]["nutrition_table"]["fat_content"]["unit"] )
            
            for i in range(len(fiber)):
                if fiber[i]["product_data"]["name"] == title and fiber[i]["product_data"]["nutrition_table"]["fiber_content"]:
                    st.subheader("Ballaststoffgehalt")
                    st.write("Anzahl der Fette: " , str(fiber[i]["product_data"]["nutrition_table"]["fiber_content"]["value"]), " in ", fiber[i]["product_data"]["nutrition_table"]["fiber_content"]["unit"] )
        

        with right : 
            for i in protItem : 
                if i["product_data"]["name"] == title and i["product_data"]["nutrition_table"]["protein_content"]:
                    st.subheader("Proteine")
                    st.write("Anzahl der Proteine: " , str(i["product_data"]["nutrition_table"]["protein_content"]["value"]), " in ", i["product_data"]["nutrition_table"]["protein_content"]["unit"] )

            for i in satfItem : 
                if i["product_data"]["name"] == title and i["product_data"]["nutrition_table"]["saturated_fat_content"]:
                    st.subheader("Gesättigte Fettsäuren")
                    st.write("Anzahl der gesättigten Fettsäuren: " , str(i["product_data"]["nutrition_table"]["saturated_fat_content"]["value"]), " in ", i["product_data"]["nutrition_table"]["saturated_fat_content"]["unit"] )
    
    elif searchItem == False :
        st.write("Dieses Produkt enthält **keine Nährwerttabelle**")