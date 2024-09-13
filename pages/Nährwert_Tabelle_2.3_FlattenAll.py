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
    print("Ladezeit aller Produkte mit Nährwert Tabelle: ", lengthnutri)

    count = 0
    countCal, countCarbo, countFat, countFiber, countSatFat, countProt, countSod, countSug = 0,0,0,0,0,0,0,0
    countJa = 0
    countNe = 0

    cal, carbo, fat, fiber, prot, satf, sod, sug = [], [], [], [], [], [], [], []

    for i in allItems : 
        count += 1

    #print(count)

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
    print("Alle Nährwerte Schleife Ladezeit: ", lengthAllNutri)



# Calculate the end time and time taken
end = time.time()
length = end - start

print("Gesamte Ladezeit: ", length)


if choice == "Nährwerte Produkte":
    
    st.title("Durchschnittliche Nährwerte aller Produkte")

    tabData, tabChart = st.tabs(["Data", "Diagram"])

    with tabData:

        colLeft, colLeftM, colRightM, colRight = st.columns(4)
        st.write("(Anzahl Produkte je Kategorie)")
        with colLeft :
            
            for c in range(len(cal)) :
                countCal += 1

            st.write("**Kalorien:**")
            st.write("**Kohlenhydrate:**")
            st.write("**Fette:**")
            st.write("**Ballaststoffe:**")
        with colLeftM : 
            st.write(str(countCal))
            st.write(str(countCarbo))
            st.write(str(countFat))
            st.write(str(countFiber))

        with colRightM :
            st.write("**Proteinen:**")
            st.write("**Gesättigten Fettsäuren:**")
            st.write("**Natrium:**")
            st.write("**Zuckern:**")
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

    title = st.text_input("Produktname eintippen", "Sweet Family Rohrzucker-Sticks 250g")
    
    container = st.container(border = True)

    prodName, prodCal, prodCarb, prodFat, prodFib, prodProt, prodSatFat, prodSod, prodSug = [], [],[],[],[],[],[],[],[]

    with container:
        st.write(f"Das ausgewählte Produkt ist:&nbsp; **{title}**")
        st.write("None : Der angegebene Nährwert existiert nicht")


    for i in allItems : 
        full_name = i["product_data/name"]
        search_name = full_name.find(title)
        shop_url = i["shop_url"]
        try: 
            if search_name != -1 :
                prodName.append(i["product_data/name"])
                try:
                    if i["product_data/nutrition_table/calories/calories_kcal/value"] or i["product_data/nutrition_table/calories/calories_kcal/value"] == 0:
                        prodCal.append(i["product_data/nutrition_table/calories/calories_kcal/value"])
                except:
                    prodCal.append(None)
                    pass
                try:
                    if i["product_data/nutrition_table/carbohydrate_content/value"] or i["product_data/nutrition_table/carbohydrate_content/value"] == 0:
                        prodCarb.append(i["product_data/nutrition_table/carbohydrate_content/value"])
                except:
                    prodCarb.append(None)
                    pass
                try:
                    if i["product_data/nutrition_table/fat_content/value"] or i["product_data/nutrition_table/fat_content/value"] == 0:
                        prodFat.append(i["product_data/nutrition_table/fat_content/value"])
                except:
                    prodFat.append(None)
                    pass
                try:
                    if i["product_data/nutrition_table/fiber_content/value"] or i["product_data/nutrition_table/fiber_content/value"] == 0:
                        prodFib.append(i["product_data/nutrition_table/fiber_content/value"])
                except:
                    prodFib.append(None)
                    pass
                try:
                    if i["product_data/nutrition_table/protein_content/value"] or i["product_data/nutrition_table/protein_content/value"] == 0:
                        prodProt.append(i["product_data/nutrition_table/protein_content/value"])
                except:
                    prodProt.append(None)
                    pass
                try:
                    if i["product_data/nutrition_table/saturated_fat_content/value"] or i["product_data/nutrition_table/saturated_fat_content/value"] == 0:
                        prodSatFat.append(i["product_data/nutrition_table/saturated_fat_content/value"])
                except:
                    prodSatFat.append(None)
                    pass
                try:
                    if i["product_data/nutrition_table/sodium_content/value"] or i["product_data/nutrition_table/sodium_content/value"] == 0 :
                        prodSod.append(i["product_data/nutrition_table/sodium_content/value"])
                except:
                    prodSod.append(None)
                    pass
                try:
                    if i["product_data/nutrition_table/sugar_content/value"] or i["product_data/nutrition_table/sugar_content/value"] == 0:
                        prodSug.append(i["product_data/nutrition_table/sugar_content/value"])
                except:
                    prodSug.append(None)
                    pass
                try: 
                    if (prodSug[-1] == None) and (prodCarb[-1] == None) and (prodSod[-1] == None) and (prodSatFat[-1] == None) and (prodFat[-1] == None) and (prodFib[-1] == None) and (prodCal[-1] == None) and (prodProt[-1] == None):
                        print("popping")
                        prodSug.pop()
                        prodCarb.pop()
                        prodSod.pop()
                        prodSatFat.pop()
                        prodFat.pop()
                        prodFib.pop()
                        prodCal.pop()
                        prodProt.pop()
                        prodName.pop() 
                except:
                    pass
                
        except : 
            pass
    
    #"nutrition_table" : {"$exists" : False}
    print("Name: ",len(prodName))
    print("Cal: ",len(prodCal))
    print("Carb: ",len(prodCarb))
    print("Fat: ",len(prodFib))
    print("Fib: ",len(prodFib))
    print("Prot: ",len(prodProt))
    print("SatFat: ",len(prodSatFat))
    print("Sodium: ",len(prodSod))
    print("Sug: ",len(prodSug))


    dt = pd.DataFrame({
        "Name" : prodName,
        "Kalorien" :  prodCal,
        "Kohlenhydrate" : prodCarb,
        "Fat" : prodFat,
        "Fiber" : prodFib,
        "Proteine" : prodProt,
        "Sat_Fat" : prodSatFat,
        "Sodium" : prodSod,
        "Sugar" : prodSug

        })

    st.dataframe(dt,
            column_config={
                "Name" : "Produktname",
                "Kalorien" : "Kalorien in kcal",
                "Kohlenhydrate" : "Kohlenhydrate in g",
                "Fat" : "Fette in g",
                "Fiber" : "Ballaststoffe in g",
                "Proteine" : "Proteine in g",
                "Sat_Fat" : "Gesättigte Fettsäuren in g",
                "Sodium" : "Natrium in g",
                "Sugar" : "Zucker in g"
            }, 
            use_container_width = True,
            hide_index = True,)

    
   