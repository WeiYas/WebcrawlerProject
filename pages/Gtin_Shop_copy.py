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

st.title("Produkte mit GTIN")
st.markdown('<style>h1{font-size:25px;} h3{font-size:20px;}</style>', unsafe_allow_html=True)

choice = st.sidebar.radio(
    "Wähle Ansicht",
    ["GTIN je Shop", "Gleiche Produkte 2er Shops"]
)
    # ------ Produkte Gtin ja ----------

#st.write(len(options))
with st.spinner('Daten werden geladen') :
    #SHOPS
    @st.cache_data(ttl=600,show_spinner = False)
    def get_data():
        db = client.mydb
        items = db.all_flatten.find({},{"shop_url":1, "product_data/gtin":1 , "product_data/name":1})
        items = list(items)
        return items

    @st.cache_data(ttl=600,show_spinner = False)
    def get_data_no_flatten() :
        db = client.mydb
        items = db.mycollection.find({"completeness" : {"$exists" : True}},{"_id":0, "completeness":1, "shop_url" : 1})
        items = list(items)
        return items

    items = get_data()
    #items_noflatten = get_data_no_flatten()

    count_dict_url = {}

    for key in items :
        if key["shop_url"] not in count_dict_url :
            count_dict_url[key["shop_url"]] = 1
        else:
            count_dict_url[key["shop_url"]] += 1

    #print(count_dict_complete)

    url_list = list(count_dict_url)

    shopsName = []
    produkteAnzahl = []
    completenessAnzahl = []

    for item in range(len(url_list)) : 
        shopsName.append(url_list[item])

    if choice == "Gleiche Produkte 2er Shops" :
        options = st.multiselect(
            "Wähle Geschäfte und zeige welche Produkte in diesen gleichzeitig zur Verfügung stehen",
            shopsName)
        st.write("Nur Produkte mit registriertem GTIN können angezeigt werden")

        # mehr als 2 shops

        if len(options) == 2 :
            with st.spinner('Daten werden geladen...'):

                
                numShop1, numShop2 = 0,0

                print(" ")
                print(shopsName)
                print(" ")
                print(options)
                print(" ")

                for i in range(len(options)) : 
                    for s in range(len(shopsName)) :
                        if options[0] == shopsName[s] :
                            numShop1 = options[0]
                        if options[1] == shopsName[s] :
                            numShop2 = options[1]

                print("Shops:" , numShop1, " and ",numShop2)
                print(" ")

                arr1, arr2 = [], []     
                arrSame1,arrSame2 = [],[]
                name0, name1 = [] , []


                for i in range(len(options)):
                    for item in items :
                        if item["shop_url"] ==options[i] and options[i] == numShop1 :
                            arr1.append(item["product_data/gtin"])

                        elif item["shop_url"] == numShop2 and options[i] == numShop2 :
                            arr2.append(item["product_data/gtin"])

                print("FirstARR:" ,len(arr1))
                print("SecondARR:", len(arr2))
                
                a = np.array(arr1)
                b = np.array(arr2)
                arrSame1 = np.intersect1d(a,b)

                print(len(arrSame1))

                lenG = len(arrSame1)
            
                st.subheader("Diese Produkte gibt es in beiden Geschäften")
                #print(arrSameE)
                #print(arrSameG)
                
                st.write("Anzahl gleicher Produkte: " ,str(lenG))

                nameProd1 = []
                nameProd2 = []
                nameShop1 = []
                nameShop2 = []

                

                dt = pd.DataFrame({
                "GTIN" : arrSame1,

                })

                st.dataframe(dt,
                        column_config={
                            "GTIN" : "GTIN"
                        }, 
                        use_container_width = True,
                        hide_index = True,)
    if choice == "GTIN je Shop" :   
        count_dict_gtin = {}

        for key in items :
            if key["shop_url"] not in count_dict_gtin :
                count_dict_gtin[key["shop_url"]] = key["product_data/gtin"]
            else:
                count_dict_gtin[key["shop_url"]] += key["product_data/gtin"]

        #print(count_dict_complete)

        gtin_list = list(count_dict_gtin)
        countGTIN = []
        countAll = 0
        average = []

        for item in range(len(url_list)) : 
            countGTIN.append(count_dict_url[url_list[item]])
            produkteAnzahl.append(count_dict_url[url_list[item]])
            average.append((count_dict_url[url_list[item]]/count_dict_url[url_list[item]])*100)

    #Completeness DURCHSCHNITT


    # --- TABELLE ---
    
        dt = pd.DataFrame({
            "shopname" : shopsName,
            "gtin" : countGTIN ,
            "prozent" : average
        })

        st.dataframe(dt,
                    column_config={
                        "shopname":"Shop",
                        "gtin" : "Anzahl Produkte mit GTIN",
                        "prozent" : "GTIN vorhanden in %"  
                    }, 
                    hide_index = True,)




                



