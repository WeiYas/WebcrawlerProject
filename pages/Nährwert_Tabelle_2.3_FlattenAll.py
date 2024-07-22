import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

choice = st.sidebar.radio(
    "Auswahl zum Anzeigen",
    ["Nährwerte Produkte", "Nährwert ein Produkt"])

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

    for i in allItems : 
        count += 1

    print(count)

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
                countCarbo += 1
                
        except :
            pass
        try : 
            if item["product_data/nutrition_table/fat_content/value"]:
                fat.append(item["product_data/nutrition_table/fat_content/value"])
                countFat += 1
                
        except :
            pass
        try : 
            if item["product_data/nutrition_table/fiber_content/value"] : 
                fiber.append(item["product_data/nutrition_table/fiber_content/value"])
                countFiber += 1
                
        except :
            pass
        try : 
            if item["product_data/nutrition_table/protein_content/value"] :
                prot.append(item["product_data/nutrition_table/protein_content/value"])
                countProt += 1
                
        except :
            pass
        try : 
            if item["product_data/nutrition_table/saturated_fat_content/value"]:
                satf.append(item["product_data/nutrition_table/saturated_fat_content/value"])
                countSatFat += 1
        except :
            pass
        try : 
            if item["product_data/nutrition_table/sodium_content/value"]:
                sod.append(item["product_data/nutrition_table/sodium_content/value"])
                countSod += 1
        except :
            pass
        try : 
            if item["product_data/nutrition_table/sugar_content/value"]:
                sug.append(item["product_data/nutrition_table/sugar_content/value"])
                countSug += 1
        except :
            pass
    
    endAllNutri = time.time()
    lengthAllNutri = endAllNutri - startAllNutri
    st.write("Alle Nährwerte Schleife Ladezeit: ", lengthAllNutri)



# Calculate the end time and time taken
end = time.time()
length = end - start

st.write("Gesamte Ladezeit: ", length)


if choice == "Nährwerte Produkte":
    
    st.title("Durchschnittliche Nährwerte aller Produkte")

    tabData, tabChart = st.tabs(["Data", "Diagram"])

    with tabData:

        colLeft, colLeftM, colRightM, colRight = st.columns(4)

        with colLeft :

            for c in range(len(cal)) :
                countCal += 1

            st.write("**Kalorien**")
            st.write("**Kohlenhydrate**")
            st.write("**Fette**")
            st.write("**Ballaststoffe**")
        with colLeftM : 
            st.write(str(countCal))
            st.write(str(countCarbo))
            st.write(str(countFat))
            st.write(str(countFiber))

        with colRightM :
            st.write("**Proteinen**")
            st.write("**Gesättigten Fettsäuren**")
            st.write("**Natrium**")
            st.write("**Zuckern**")
        with colRight:
            st.write(str(countProt))
            st.write(str(countSatFat))
            st.write(str(countSod))
            st.write(str(countSug))
    with tabChart:

        chart_data = pd.DataFrame({
            'Nährwerte': ["Kalorien","Kohlenhydrate", "Fette" , "Ballaststoffe", "Proteine", "Ges.Fettsäuren", "Natrium","Zucker"],
            'Anzahl Nährwertangabe':[countCal,countCarbo,countFat,countFiber,countProt,countSatFat,countSod,countSug]})
        c = ( 
           alt.Chart(chart_data).mark_bar().encode(x='Nährwerte',y='Anzahl Nährwertangabe')
        )
        st.altair_chart(c, use_container_width=True)


if choice == "Nährwert ein Produkt" :
    st.title("Nährwerte eines ausgewählten Produktes")

    #Anzeigen Nährstoffe eines Produktes

    title = st.text_input("Produktname eintippen", "Holle frucht pur Pouchy Birne & Aprikose - Bio - 90g - vekoop.de")
    
    container = st.container(border = True)

    with container:
        st.write(f"Das ausgewählte Produkt ist:&nbsp; **{title}**")
        edeka_arr , vekoop_arr = [] , []

        for i in allItems : 
            full_name = i["product_data/name"]
            search_name = full_name.find(title)
            shop_url = i["shop_url"]

            #dies anstatt Preis mit Nährwerten !! 

            try: 
                if search_name != -1 and i["product_data/price"]:
                    st.write("**Name:** " ,full_name)
                    st.write("Preis: ",i["product_data/price"] )
                elif  search_name != -1 and not i["product_data/price"]: 
                    st.write("**Name:** " ,full_name)
                    st.write("Kein Preis vorhanden")
            except : 
                pass

    
   