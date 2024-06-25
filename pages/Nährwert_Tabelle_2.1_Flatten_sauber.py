import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

choice = st.sidebar.radio(
    "Auswahl zum Anzeigen",
    ["Produkte vorhanden", "Nährwerte Produkte", "Nährwert ein Produkt"])

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()

st.markdown('<style>h1{font-size:25px;} h3{font-size:20px;}</style>', unsafe_allow_html=True)
st.title("Nährwerte Übersicht")

# Calculate the start time
start = time.time()

# Code here

with st.spinner('Daten werden geladen') :
    @st.cache_data(ttl=600,show_spinner = False)
    def get_data_nutri():
        db = client.mydb
        items = db.nutrition_flatten.find({},{"_id" : 0})
        items = list(items)
        return items

    @st.cache_data(ttl=600,show_spinner = False)
    def get_data():
        db = client.mydb
        items = db.mycollection.find({},{"_id": 0,  "shop_url" : 1 , "product_data" :{ "nutrition_table" : 1 , "name" : 1} })
        items = list(items)
        return items

    startnutri = time.time()
    nutri = get_data_nutri()
    endnutri = time.time()
    lengthnutri = endnutri - startnutri
    st.write("Ladezeit aller Produkte mit Nährwert Tabelle: ", lengthnutri)

    startall = time.time()
    allItems = get_data()
    endall = time.time()
    lengthall = endall - startall
    st.write("Ladezeit alle Produkte: ", lengthall)

    cal, carbo, fat, fiber, prot, satf, sod, sug = [], [], [], [], [], [], [], []

    for item in nutri : 
        try : 
            if item["calories.calories_kcal.value"] :
                cal.append(item["calories.calories_kcal.value"])
        except :
            pass
        try : 
            if item["carbohydrate_content.value"]:
                carbo.append(item["carbohydrate_content.value"])
        except :
            pass
        try : 
            if item["fat_content.value"]:
                fat.append(item["fat_content.value"])
        except :
            pass
        try : 
            if item["fiber_content.value"] : 
                fiber.append(item["fiber_content.value"])
        except :
            pass
        try : 
            if item["protein_content.value"] :
                prot.append(item["protein_content.value"])
        except :
            pass
        try : 
            if item["saturated_fat_content.value"]:
                satf.append(item["saturated_fat_content.value"])
        except :
            pass
        try : 
            if item["sodium_content.value"]:
                sod.append(item["sodium_content.value"])
        except :
            pass
        try : 
            if item["sugar_content.value"]:
                sug.append(item["sugar_content.value"])
        except :
            pass



    count = 0
    countJa = 0
    countNe = 0

# Calculate the end time and time taken
end = time.time()
length = end - start

st.write("Gesamte Ladezeit: ", length)


for i in nutri :
    countJa += 1

for i in allItems : 
    count += 1

countNe = count - countJa

#Attribute Anzeigen rechnen


#Anzeige Browser

if choice == "Produkte vorhanden":
    st.title("Nährwerttabelle existiert")
    chart_data = pd.DataFrame({
    'Nährwert Tabelle vorhanden': ["ja","nein"],
    'Anzahl Produkte':[countJa,countNe]
    })
    c = ( 
        alt.Chart(chart_data).mark_bar().encode(x='Nährwert Tabelle vorhanden',y='Anzahl Produkte')
        )
    st.altair_chart(c, use_container_width=True)

if choice == "Nährwerte Produkte":
    
    st.title("Durchschnittliche Nährwerte aller Produkte")

    tabData, tabChart = st.tabs(["Data", "Diagram"])

    with tabData:

        colLeft, colRight = st.columns(2)

        with colLeft :

            countCal = 0
            countCarb = 0
            countfat = 0
            countfib = 0

            for i in cal :
                countCal += 1
            for i in carbo :
                countCarb += 1
            for i in fat :
                countfat += 1
            for i in fiber :
                countfib += 1


            st.write("**Produkte mit Kalorien**" , str(countCal))
            st.write("**Produkte mit Kohlenhydraten**",str(countCarb))
            st.write("**Produkte mit Fetten**" , str(countfat))
            st.write("**Produkten mit Ballaststoffen**" , str(countfib))
        
        with colRight :

            countprot = 0
            for item in prot:
                countprot += 1
            
            countsf = 0
            for item in satf:
                countsf += 1
            
            countsod = 0
            for item in sod:
                countsod += 1
            
            countsug = 0
            for item in sug:
                countsug += 1
            
            st.write("**Produkte mit Proteinen**" , str(countprot))
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


if choice == "Nährwert ein Produkt" :
    st.title("Nährwerte eines ausgewählten Produktes")

    #Anzeigen Nährstoffe eines Produktes

    title = st.text_input("Produktname eintippen", "Holle frucht pur Pouchy Birne & Aprikose - Bio - 90g - vekoop.de")
    
    container = st.container(border = True)

    with container:
        st.write("Work in progress")