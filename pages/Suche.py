import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()

with st.spinner('Daten werden geladen') :

    @st.cache_data(ttl=600, show_spinner=False)
    def get_data():
        db = client.mydb
        items = db.all_flatten.find({},{"product_data" : {"nutrition_table" : 0}})
        items = list(items)
        return items

    @st.cache_data(ttl=600, show_spinner=False)
    def get_data_noflat():
        db = client.mydb
        items = db.mycollection.find({},{"product_data" : {"nutrition_table" : 0}})
        items = list(items)
        return items

    items = get_data()
    itemsNoFlat = get_data_noflat()

    count_dict_url = {}
    count_dict_complete = {}

    for key in items :
        if key["shop_url"] not in count_dict_url :
            count_dict_url[key["shop_url"]] = 1
        else:
            count_dict_url[key["shop_url"]] += 1

    for key in itemsNoFlat :
        if key["shop_url"] not in count_dict_complete :
            count_dict_complete[key["shop_url"]] = key["completeness"]
        else:
            count_dict_complete[key["shop_url"]] += key["completeness"]

    #print(count_dict_complete)

    url_list = list(count_dict_url)
    complete_list = list(count_dict_complete)

    shopsName = []
    produkteAnzahl = []
    completenessAnzahl = []

    for item in range(len(url_list)) : 
        shopsName.append(url_list[item])
        produkteAnzahl.append(count_dict_url[url_list[item]])
        average = count_dict_complete[url_list[item]]/count_dict_url[complete_list[item]]
        completenessAnzahl.append(average)

    container = st.container(border = True)

    with container:
        title = st.text_input(
            "Suche nach einem Produkt",
            "Sun Rice Schokopuffreis Original 250g",
            key="placeholder",
        )
        st.write(f"Das ausgewählte Produkt ist:&nbsp; **{title}**")

    sName ,pName, gtinNumb, prodNumb = [],[], [], []

    for i in items : 
        full_name = i["product_data/name"]
        search_name = full_name.find(title)
        shop_url = i["shop_url"]

        #dies anstatt Preis mit Nährwerten !! 

        try: 
            if search_name != -1 and i["_id"]:
                sName.append(i["shop_url"])
                pName.append(i["product_data/name"])
                if i["product_data/gtin"] :
                    gtinNumb.append(i["product_data/gtin"])
                else :
                    gtinNumb.append(None)
                if i["product_data/product_number"] :
                    prodNumb.append(i["product_data/product_number"])
                else :
                    prodNumb.append(None)
                
                #st.write("Preis: ",i["product_data/price"] )
            elif  search_name != -1 and not i["product_data/price"]: 
                st.write("Auswahl konnt nicht gefunden werden")
        except : 
            pass

    dt = pd.DataFrame({
    "produktName" :  pName,
    "shopname" : sName,
    "gtin" : gtinNumb,
    "product Number" : prodNumb 
    })

    st.dataframe(dt,
            column_config={
                "produktName" : "Produktname",
                "shopname":"Shop",
                "gtin" : "GTIN",
                "product Number" : "Produktnummer"
            }, 
            hide_index = True,)
    

        
    