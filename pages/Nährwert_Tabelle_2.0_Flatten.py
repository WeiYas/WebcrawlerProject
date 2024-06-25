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
        
    @st.cache_data(ttl=600,show_spinner = False)
    def get_data_cal():
        db = client.mydb
        items = db.nutrition_flatten.find({'$expr': { '$getField': 'calories.calories_kcal.value' }},{})
        items = list(items)
        return items

    @st.cache_data(ttl=600,show_spinner = False)
    def get_data_carbo():
        db = client.mydb
        items = db.nutrition_flatten.find({'$expr': { '$getField': 'carbohydrate_content.value' }},{})
        items = list(items)
        return items

    @st.cache_data(ttl=600,show_spinner = False)
    def get_data_fat():
        db = client.mydb
        items = db.nutrition_flatten.find({'$expr': { '$getField': 'fat_content.value' }},{})
        items = list(items)
        return items

    @st.cache_data(ttl=600,show_spinner = False)
    def get_data_fiber():
        db = client.mydb
        items = db.nutrition_flatten.find({'$expr': { '$getField': 'fiber_content.value' }},{})
        items = list(items)
        return items

    @st.cache_data(ttl=600,show_spinner = False)
    def get_data_prot():
        db = client.mydb
        items = db.nutrition_flatten.find({"$expr": { "$getField": "protein_content.value" }},{})
        items = list(items)
        return items

    @st.cache_data(ttl=600,show_spinner = False)
    def get_data_satf():
        db = client.mydb
        items = db.nutrition_flatten.find({'$expr': { '$getField': 'saturated_fat_content.value' }},{})
        items = list(items)
        return items

    @st.cache_data(ttl=600,show_spinner = False)
    def get_data_sod():
        db = client.mydb
        items = db.nutrition_flatten.find({'$expr': { '$getField': 'sodium_content.value' }},{})
        items = list(items)
        return items

    @st.cache_data(ttl=600,show_spinner = False)
    def get_data_sug():
        db = client.mydb
        items = db.nutrition_flatten.find({"$expr": { '$getField': 'sugar_content.value' }},{})
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

    #Kalorien-variable und Ladezeit
    startcal = time.time()
    cal = get_data_cal()
    endcal = time.time()
    lengthcal = endcal - startcal
    st.write("Ladezeit Kalorien: ", lengthcal)

    #Kohlenhydrate-variable und Ladezeit
    startcarb = time.time()
    carbo = get_data_carbo()
    endcarb = time.time()
    lengthcarb = endcarb - startcarb
    st.write("Ladezeit Carbohydrate: ", lengthcarb)

    startfat = time.time()
    fat = get_data_fat()
    endfat = time.time()
    lengthfat = endfat - startfat
    st.write("Ladezeit Fette: ", lengthfat)
    
    startfiber = time.time()
    fiber = get_data_fiber()
    endfiber = time.time()
    lengthfiber = endfiber - startfiber
    st.write("Ladezeit Ballaststoffe: ", lengthfiber)

    startprot = time.time()
    protItem = get_data_prot()
    endprot = time.time()
    lengthprot = endprot - startprot
    st.write("Ladezeit Proteine: ", lengthprot)

    startsatf = time.time()
    satfItem = get_data_satf()
    endsatf = time.time()
    lengthsatf = endsatf - startsatf
    st.write("Ladezeit Gesättigte Fettsäuren: ", lengthsatf)
    
    startsod = time.time()
    sodItem = get_data_sod()
    endsod = time.time()
    lengthsod = endsod - startsod
    st.write("Ladezeit Natrium: ", lengthsod)

    startsug = time.time()
    sugItem = get_data_sug()
    endsug = time.time()
    lengthsug = endsug - startsug
    st.write("Ladezeit Zuckergehalt: ", lengthsug)
    

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
            for item in protItem:
                countprot += 1
            
            countsf = 0
            for item in satfItem:
                countsf += 1
            
            countsod = 0
            for item in sodItem:
                countsod += 1
            
            countsug = 0
            for item in sugItem:
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