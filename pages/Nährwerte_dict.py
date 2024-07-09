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
        items = db.all_flatten.find({},{"_id" : 0, "shop_url":1})
        items = list(items)
        return items
    
    nutri_list = get_data_nutri()
    count_dict = {}

    for key in nutri_list :
        if key["shop_url"] not in count_dict :
            count_dict[key["shop_url"]] = 1
        else:
            count_dict[key["shop_url"]] += 1

    print(count_dict)

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
                countCal += 1
                
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
            countJa +=1
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
        st.write(f"Das ausgewählte Produkt ist:&nbsp; **{title}**")
        edeka_arr , vekoop_arr = [] , []

        for i in allItems : 
            full_name = i["product_data/name"]
            search_name = full_name.find(title)
            shop_url = i["shop_url"]

            try: 
                if search_name != -1 and shop_url == "https://www.edeka24.de/":
                    edeka_arr.append(i["product_data/name"])
                    #print(edeka_arr)
            except : 
                pass

            try:
                if search_name != -1 and shop_url == "https://www.vekoop.de/":
                    vekoop_arr.append(i["product_data/name"])
                    #print(vekoop_arr)
            except:
                pass
    
    e = st.toggle("Edeka Produkte")
    v = st.toggle("Vekoop Produkte")

    if e :
        st.write("**Edeka Produkte**")
        for i in range(len(edeka_arr)) : 
            st.write("- ", edeka_arr[i] )
    if v :
        st.write("**Vekoop Produkte**")
        for i in range(len(vekoop_arr)) :
            st.write("- ", vekoop_arr[i])
            


    searchItem = False