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
st.title("Insgesamte Preisverteilung")

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
    countE = 0
    countV = 0
    arr = []

    count_dict_url = {}
    count_dict_complete = {}

    for key in items :
        if key["shop_url"] not in count_dict_url :
            count_dict_url[key["shop_url"]] = 1
        else:
            count_dict_url[key["shop_url"]] += 1

    url_list = list(count_dict_url)
    shopsName = []
    produkteAnzahl = []
    countShops = 0

    range1,range2, range3, range4 , range5 , range6 , range7, range8, range9 , range10,range11,range12,range13,range14,range15,range16,range17,range18,range19,range20,range21,range22,range23,range24,range25,range26,range27 = 0, 0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0

    for item in range(len(url_list)) : 
        shopsName.append(url_list[item])
        produkteAnzahl.append(count_dict_url[url_list[item]])
        countShops +=1

    x = 0

    for item in items :
        try:
            if int(float(item["product_data/price"])) > 0 and int(float(item["product_data/price"])) <= 1 :
                range1 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 1 and int(float(item["product_data/price"])) <= 2 :
                range2 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 2 and int(float(item["product_data/price"])) <= 3 :
                range3 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 3 and int(float(item["product_data/price"])) <= 4 :
                range4 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 4 and int(float(item["product_data/price"])) <= 5 :
                range5 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 5 and int(float(item["product_data/price"])) <= 6 :
                range6 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 6 and int(float(item["product_data/price"])) <= 7 :
                range7 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 7 and int(float(item["product_data/price"])) <= 8 :
                range8 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 8 and int(float(item["product_data/price"])) <= 9 :
                range9 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 9 and int(float(item["product_data/price"])) <= 10 :
                range10 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 10 and int(float(item["product_data/price"])) <= 15 :
                range11 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 15 and int(float(item["product_data/price"])) <= 20 :
                range12 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 20 and int(float(item["product_data/price"])) <= 25 :
                range13 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 25 and int(float(item["product_data/price"])) <= 30 :
                range14 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 30 and int(float(item["product_data/price"])) <= 35 :
                range15 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 35 and int(float(item["product_data/price"])) <= 40 :
                range16 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 40 and int(float(item["product_data/price"])) <= 45 :
                range17 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 45 and int(float(item["product_data/price"])) <= 50 :
                range18 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 50 and int(float(item["product_data/price"])) <= 60 :
                range19 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 60 and int(float(item["product_data/price"])) <= 70 :
                range20 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 70 and int(float(item["product_data/price"])) <= 80 :
                range21 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 80 and int(float(item["product_data/price"])) <= 90 :
                range22 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 90 and int(float(item["product_data/price"])) <= 100 :
                range23 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 100 and int(float(item["product_data/price"])) <= 200 :
                range24 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 200 and int(float(item["product_data/price"])) <= 300 :
                range25 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 300 and int(float(item["product_data/price"])) <= 400 :
                range26 += 1
        except:
            pass
        try:
            if int(float(item["product_data/price"])) > 400 and int(float(item["product_data/price"])) <= 500 :
                range27 += 1
        except:
            pass

    preiseArr = ["[0€ - 1€]","]1€ - 2€]","]2€ - 3€]","]3€ - 4€]","]4€ - 5€]","]5€ - 6€]","]6€ - 7€]","]7€ - 8€]","]8€ - 9€]","]9€ - 10€]","]10€ - 15€]","]15€ - 20€]","]20€ - 25€]","]25€ - 30€]","]30€ - 35€]","]35€ - 40€]","]40€ - 45€]","]45€ - 50€]","]50€ - 60€]","]60€ - 70€]","]70€ - 80€]","]80€ - 90€]","]90€ - 100€]","]100€ - 200€]","]200€ - 300€]","]300€ - 400€]","]400€ - 500€]"]

    chart_data = pd.DataFrame({'Preisbereich': preiseArr, 
                            'Anzahl Produkte':[range1,range2, range3, range4 , range5 , range6 , range7, range8, range9 , range10,range11,range12,range13,range14,range15,range16,range17,range18,range19,range20,range21,range22,range23,range24,range25,range26,range27]})

    c = ( 
        alt.Chart(chart_data).mark_bar().encode(alt.X('Preisbereich',sort = preiseArr,axis=alt.Axis(labelAngle=0)) ,alt.Y('Anzahl Produkte',axis=alt.Axis(labelAngle=0)))
        )
    st.altair_chart(c, use_container_width=True)
