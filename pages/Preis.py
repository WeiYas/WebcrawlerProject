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

radiochoice = st.sidebar.radio( "Auswahl zum Anzeigen",
    ["Preisbereiche je Shop", "Preisverteilung aller Shops"])

st.markdown('<style>h1{font-size:25px;} h3{font-size:20px;}</style>', unsafe_allow_html=True)
st.title("Anzahl Produkte in einer spezifischen Preisgruppe")

container = st.container(border=True)

with st.spinner('Daten werden geladen') :

    @st.cache_data(ttl=600,show_spinner=False)
    def get_data():
        db = client.mydb
        items = db.all_flatten.find({},{})
        items = list(items)
        return items

    items = get_data()
    count = 0
    arr = []

    count_dict_url = {}
    count_dict_complete = {}

    for key in items :
        if key["shop_url"] not in count_dict_url :
            count_dict_url[key["shop_url"]] = 1
        else:
            count_dict_url[key["shop_url"]] += 1

    #print(count_dict_url)

    for key in items :
        try :
            if key["product_data/price"] :
                if key["shop_url"] not in count_dict_complete :
                    count_dict_complete[key["shop_url"]] = float(key["product_data/price"])
                else:
                    count_dict_complete[key["shop_url"]] += float(key["product_data/price"])
        except:
            if key["shop_url"] not in count_dict_complete :
                count_dict_complete[key["shop_url"]] = 0
            else:
                count_dict_complete[key["shop_url"]] += 0
            pass

    #print(count_dict_complete)
    url_list = list(count_dict_url)
    complete_list = list(count_dict_complete)

    #print(complete_list)

    shopsName , produkteAnzahl, priceDurchschnitt = [] , [], []
    countShops = 0
    average = 0

    #print(count_dict_complete)
    #print(count_dict_url)

    for item in range(len(url_list)) : 
        shopsName.append(url_list[item])
        produkteAnzahl.append(count_dict_url[url_list[item]])
        countShops +=1
        print(count_dict_complete[url_list[item]])
        print(count_dict_url[complete_list[item]])
        try :
            average = count_dict_complete[url_list[item]]/count_dict_url[complete_list[item]]

        except:
            pass
        priceDurchschnitt.append(average)
        


    if radiochoice == "Preisbereiche je Shop":
        with container: 
            option = st.selectbox(
            "Wählen sie einen Shop aus: ", shopsName, placeholder="Shopauswahl...",index=None)

            rangeS = st.slider('Wähle einen Preisbereich:', value = [0,500])
            
            st.write("- **Ausgewählter Bereich:**", str(rangeS[0])," bis " , str(rangeS[1])," EUR")

        for i in range(len(items)) : 
            try:
                if items[i]["product_data/price"] :
                    price = items[i]["product_data/price"]
                    if int(float(price)) <= rangeS[1] and int(float(price)) >= rangeS[0] :
                        count += 1
            except:
                pass

        priceShop = 0
        countTotal = 0
        countShop = 0

        if option != None :
            for i in range(len(items)): 
                for item in items :
                    try: 
                        if option == shopsName[i] and option == item["shop_url"]:
                            countTotal += 1
                            #print(shopsName[i])
                            priceShop = item["product_data/price"]
                            #print(countTotal)
                            if int(float(priceShop)) <= rangeS[1] and int(float(priceShop)) >= rangeS[0] :
                                countShop += 1
                    except: 
                        pass

                if produkteAnzahl[i] == countTotal :
                    break

        st.subheader(option)
        st.write("Anzahl Produkte in Preisbereich:", countShop)
        chart_data = pd.DataFrame({'name': ["Ausgewählte","Totale Anzahl"], 'number of products':[countShop,countTotal]})
        chart_data = chart_data.set_index('name')
        st.bar_chart(chart_data)

    elif radiochoice == "Preisverteilung aller Shops":
        dt = pd.DataFrame({
        "shopname" : shopsName ,
        "completeness" : priceDurchschnitt
        })

        st.dataframe(dt,
                column_config={
                    "shopname":"Shop",
                    "completeness" : "Preisdurchschnitt"
                }, 
                hide_index = True,)