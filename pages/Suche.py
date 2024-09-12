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

st.markdown('<style>h1{font-size:25px;} h3{font-size:20px;}</style>', unsafe_allow_html=True)
st.title("Suche nach Produkt")

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
        choice = st.radio(
        "Suche mit Teilnamen des Produktes oder GTIN?",
        ["Teilname des Produktes", "GTIN"])

        if choice == "Teilname des Produktes" :
            title = st.text_input(
                "Suche nach einem Produkt mit Teilnamen",
                "Suche",
                key="placeholderT",
            )
            st.write(f"Das ausgewählte Produkt ist:&nbsp; **{title}**")

        if choice == "GTIN" :
            gtinSearch = st.text_input(
                "Suche nach einem Produkt mit GTIN",
                "Suche mit GTIN",
                key="placeholderG",
            )
            st.write(f"Die GTIN des ausgewählten Produktes ist:&nbsp; **{gtinSearch}**")

    sName ,pName, gtinNumb, prodNumb, price = [],[], [], [] , []

    for i in items : 
        #dies anstatt Preis mit Nährwerten !! 
        try:
            if title :
                full_name = i["product_data/name"]
                search_name = full_name.find(title)
                shop_url = i["shop_url"]
        except :
            pass
        try: 
            if title and search_name != -1 and title != "Suche":
                sName.append(i["shop_url"])
                pName.append(i["product_data/name"])
                try : 
                    if i["product_data/gtin"] :
                        gtinNumb.append(i["product_data/gtin"])
                except:    
                    gtinNumb.append(None)
                    pass
                try : 
                    if i["product_data/product_number"] :
                        prodNumb.append(i["product_data/product_number"])
                except:
                    prodNumb.append(None)
                    pass
                try : 
                    if i["product_data/price"] :
                        price.append(i["product_data/price"])
                except :
                    price.append(None)
                    pass
                #st.write("Preis: ",i["product_data/price"] )
        except: 
            pass
        try:
            if  gtinSearch == i["product_data/gtin"]: 
                sName.append(i["shop_url"])
                pName.append(i["product_data/name"])
                try : 
                    if i["product_data/gtin"] :
                        gtinNumb.append(i["product_data/gtin"])
                except:    
                    gtinNumb.append(None)
                    pass
                try : 
                    if i["product_data/product_number"] :
                        prodNumb.append(i["product_data/product_number"])
                except:
                    prodNumb.append(None)
                    pass
                try : 
                    if i["product_data/price"] :
                        price.append(i["product_data/price"])
                except :
                    price.append(None)
                    pass
        except : 
            pass

    dt = pd.DataFrame({
    "produktName" :  pName,
    "preis" : price,
    "shopname" : sName,
    "gtin" : gtinNumb,
    "product Number" : prodNumb 
    })

    st.dataframe(dt,
            column_config={
                "produktName" : "Produktname",
                "preis" : "Preis in €" ,
                "shopname":"Shop",
                "gtin" : "GTIN",
                "product Number" : "Produktnummer"
            }, 
            hide_index = True,)
    

        
    