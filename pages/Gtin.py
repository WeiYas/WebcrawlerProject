import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import altair as alt
import array
import plotly.graph_objects as go

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()

st.title("Produkte mit Gtin")
st.markdown('<style>h1{font-size:25px;} h3{font-size:20px;}</style>', unsafe_allow_html=True)
tabAll , tabCompare = st.tabs(["Gtin Vorhanden","Produkte gleicher Gtin"])

with tabAll : 

    @st.cache_data(ttl=600)
    def get_data():
        db = client.mydb
        items = db.all_flatten.find({}, {})
        items = list(items)
        return items

    gtin = get_data()

    countGtin = 0
    countNoGtin = 0

    for i in gtin :
        try: 
            if i["product_data/gtin"] :
                countGtin += 1
        except:
            pass
        try :
            if not i["product_data/gtin"] : 
                countNoGtin += 1
        except:
            pass


    chart_data = pd.DataFrame({
    'Gtin vorhanden': ["ja","nein"],
    'Anzahl Produkte':[countGtin,countNoGtin]
    })
    # ANZEIGE AUF BROWSER

    
    st.write(" ")

    st.subheader("Wieviele Produkte besitzen einen gtin?")

    container = st.container(border = True)
    with container:
        st.write("- Anzahl von Produkten mit gtin: ", countGtin)
        st.write("- Anzahl von Produkten ohne gtin" , countNoGtin)

            #chart_data = chart_data.set_index('Gtin vorhanden')
            #st.bar_chart(chart_data)
    c = ( 
    alt.Chart(chart_data).mark_bar().encode(x='Gtin vorhanden',y='Anzahl Produkte')
    )
    st.altair_chart(c, use_container_width=True)

    onChart = st.toggle("Pie chart")
    if onChart :
        labels = 'Edeka' , 'Vekoop' , 'Globus'
        sizes = [20,30,50]
        fig1, ax1 = plt.subplots()
        ax1.pie(sizes, labels=labels, autopct='%1.1f%%',shadow=False, startangle=90)
        ax1.axis('equal')
        st.pyplot(fig1)

with tabCompare :
    # ------ Produkte Gtin ja ----------

    options = st.multiselect(
        "Wähle Geschäfte und zeige welche Produkte in diesen gleichzeitig zur Verfügung stehen",
        ["Edeka", "Vekoop","Globus", "Supermarkt24h"])
    st.write("Nur Produkte mit registriertem gtin können angezeigt werden")
    #st.write(len(options))

    @st.cache_data(ttl=600)
    def get_data():
        db = client.mydb
        items = db.all_flatten.find({}, {})
        items = list(items)
        return items

    items = get_data()

    # mehr als 2 shops

    if len(options) == 2 :
        with st.spinner('Daten werden geladen...'):

            numShop = len(options)
            urls = ["https://www.edeka24.de/","https://www.vekoop.de/", "https://www.globus.de/", "https://www.supermarkt24h.de/"]

            arrE,arrV,arrG, arrS = [],[],[],[]       
            arrSameE,arrSameV,arrSameG,arrSameS = [], [],[],[]
            name0, name1 = [] , []
            lenG = 0

            for i in range(numShop):
                for item in items :
                    if item["shop_url"] == "https://www.edeka24.de/" and options[i] == "Edeka" :
                        arrE.append(item["product_data/gtin"])
                    elif item["shop_url"] == "https://www.vekoop.de/" and options[i] == "Vekoop" :
                        arrV.append(item["product_data/gtin"])
                    elif item["shop_url"] == "https://www.globus.de/" and options[i] == "Globus" :
                        arrG.append(item["product_data/gtin"])
                    elif item["shop_url"] == "https://www.supermarkt24h.de/" and options[i] == "Supermarkt24h" :
                        arrS.append(item["product_data/gtin"])
                    

            if (options[0] == "Edeka" and options[1]=="Vekoop") or (options[1] == "Edeka" and options[0]=="Vekoop") :
                for a in range(len(arrE)):
                    for b in range(len(arrV)) :
                        if arrE[a] == arrV[b] :
                            arrSameE.append(arrE[a])
                            arrSameV.append(arrV[b])
            elif (options[0] == "Edeka" and options[1]=="Globus") or (options[1] == "Edeka" and options[0]=="Globus") :
                for a in range(len(arrE)):
                    for b in range(len(arrG)) :
                        if arrE[a] == arrG[b] :
                            arrSameE.append(arrE[a])
                            arrSameG.append(arrG[b])
            elif (options[0] == "Vekoop" and options[1]=="Globus") or (options[0] == "Globus" and options[1]=="Vekoop") :
                for a in range(len(arrV)):
                    for b in range(len(arrG)) :
                        if arrV[a] == arrG[b] :
                            arrSameV.append(arrV[a])
                            arrSameG.append(arrG[b])
            elif (options[0] == "Supermarkt24h" and options[1]=="Globus") or (options[0] == "Globus" and options[1]=="Supermarkt24h") :
                for a in range(len(arrS)):
                    for b in range(len(arrG)) :
                        if arrS[a] == arrG[b] :
                            arrSameS.append(arrS[a])
                            arrSameG.append(arrG[b])
            elif (options[0] == "Supermarkt24h" and options[1]=="Edeka") or (options[0] == "Edeka" and options[1]=="Supermarkt24h") :
                for a in range(len(arrS)):
                    for b in range(len(arrE)) :
                        if arrS[a] == arrE[b] :
                            arrSameS.append(arrS[a])
                            arrSameE.append(arrE[b])

                for i in range(len(arrSameS)) :    
                    for item in items: 
                        if item["product_data/gtin"] == arrSameS[i] and item["shop_url"] == "https://www.supermarkt24h.de/":
                            name0.append(item["product_data/name"])
                        if item["product_data/gtin"] == arrSameE[i] and item["shop_url"] == "https://www.edeka24.de/":
                            name1.append(item["product_data/name"])
                lenG = len(arrSameS)
                print(len(arrSameS))
                print(len(name0))
                print(len(name1))

                d = {'Gtin' : arrSameS, 'Name1' : name1}
                
            

                
            st.subheader("Diese Produkte gibt es in beiden Geschäften")
            #print(arrSameE)
            #print(arrSameG)
            
            st.write("Anzahl gleicher Produkte: " ,str(lenG))

            onTable = st.toggle("Zeige Daten")
            if onTable :
                df = pd.DataFrame(data = d)
                st.table(df)




            



