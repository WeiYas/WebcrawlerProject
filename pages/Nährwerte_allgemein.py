import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()

st.markdown('<style>h1{font-size:25px;} h3{font-size:20px;}</style>', unsafe_allow_html=True)
st.title("Nährwerte Übersicht")

# Calculate the start time
start = time.time()


with st.spinner('Daten werden geladen') :
    @st.cache_data(ttl=600,show_spinner = False)
    def get_data_nutri():
        db = client.mydb
        items = db.all_flatten.find({},{"_id" : 0})
        items = list(items)
        return items

    startnutri = time.time()
    allItems = get_data_nutri()
    endnutri = time.time()
    lengthnutri = endnutri - startnutri
    st.write("Ladezeit aller Produkte mit Nährwert Tabelle: ", lengthnutri)

    count = 0
    countCal, countCarbo, countFat, countFiber, countSatFat, countProt, countSod, countSug = 0,0,0,0,0,0,0,0
    countJa = 0
    countNe = 0

    cal, carbo, fat, fiber, prot, satf, sod, sug = [], [], [], [], [], [], [], []

    
    startAllNutri = time.time()
    for item in allItems : 
        try : 
            if item["product_data/nutrition_table/calories/calories_kcal/value"] :
                cal.append(item["product_data/nutrition_table/calories/calories_kcal/value"])
 
        except :
            pass
        try : 
            if item["product_data/nutrition_table/carbohydrate_content/value"]:
                carbo.append(item["product_data/nutrition_table/carbohydrate_content/value"])
         
        except :
            pass
        try : 
            if item["product_data/nutrition_table/fat_content/value"]:
                fat.append(item["product_data/nutrition_table/fat_content/value"])
            
        except :
            pass
        try : 
            if item["product_data/nutrition_table/fiber_content/value"] : 
                fiber.append(item["product_data/nutrition_table/fiber_content/value"])
    
        except :
            pass
        try : 
            if item["product_data/nutrition_table/protein_content/value"] :
                prot.append(item["product_data/nutrition_table/protein_content/value"])

        except :
            pass
        try : 
            if item["product_data/nutrition_table/saturated_fat_content/value"]:
                satf.append(item["product_data/nutrition_table/saturated_fat_content/value"])

        except :
            pass
        try : 
            if item["product_data/nutrition_table/sodium_content/value"]:
                sod.append(item["product_data/nutrition_table/sodium_content/value"])
        except :
            pass
        try : 
            if item["product_data/nutrition_table/sugar_content/value"]:
                sug.append(item["product_data/nutrition_table/sugar_content/value"])
        except :
            pass
    
    endAllNutri = time.time()
    lengthAllNutri = endAllNutri - startAllNutri
    st.write("Alle Nährwerte Schleife Ladezeit: ", lengthAllNutri)


countCal = len(cal)
countCarbo = len(carbo)
countFat = len(fat)
countFiber = len(fiber)
countSatFat = len(satf)
countProt = len(prot)
countSod = len(sod)
countSug = len(sug)
count = len(allItems)
countJa = countCal
countNe = count-countJa


# Calculate the end time and time taken
end = time.time()
length = end - start

st.write("Gesamte Ladezeit: ", length)


#Anzeige Browser

st.title("Produkte mit Nährwerttabelle")
chart_data = pd.DataFrame({
'Nährwert Tabelle vorhanden': ["ja","nein"],
'Anzahl Produkte':[countJa,countNe]
})
c = ( 
    alt.Chart(chart_data).mark_bar().encode(x='Nährwert Tabelle vorhanden',y='Anzahl Produkte')
    )
st.altair_chart(c, use_container_width=True)