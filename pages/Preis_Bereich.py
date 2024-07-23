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

@st.cache_data(ttl=600)
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

range05,range510, range1015, range1520 , range2025 , range2530 , range3035, range3540, range4045 , range4550,range50100,range100200,range200300,range300400,range400500 = 0 , 0, 0,0,0,0,0,0,0,0,0,0,0,0,0

for item in range(len(url_list)) : 
    shopsName.append(url_list[item])
    produkteAnzahl.append(count_dict_url[url_list[item]])
    countShops +=1

for item in items :
    try:
        if int(float(item["product_data/price"])) > 0 and int(float(item["product_data/price"])) <= 5 :
            range05 += 1
    except:
        pass
    try:
        if int(float(item["product_data/price"])) > 5 and int(float(item["product_data/price"])) <= 10 :
            range510 += 1
    except:
        pass
    try:
        if int(float(item["product_data/price"])) > 10 and int(float(item["product_data/price"])) <= 15 :
            range1015 += 1
    except:
        pass
    try:
        if int(float(item["product_data/price"])) > 15 and int(float(item["product_data/price"])) <= 20 :
            range1520 += 1
    except:
        pass
    try:
        if int(float(item["product_data/price"])) > 20 and int(float(item["product_data/price"])) <= 25 :
            range2025 += 1
    except:
        pass
    try:
        if int(float(item["product_data/price"])) > 25 and int(float(item["product_data/price"])) <= 30 :
            range2530 += 1
    except:
        pass
    try:
        if int(float(item["product_data/price"])) > 30 and int(float(item["product_data/price"])) <= 35 :
            range3035 += 1
    except:
        pass
    try:
        if int(float(item["product_data/price"])) > 35 and int(float(item["product_data/price"])) <= 40 :
            range3540 += 1
    except:
        pass
    try:
        if int(float(item["product_data/price"])) > 40 and int(float(item["product_data/price"])) <= 45 :
            range4045 += 1
    except:
        pass
    try:
        if int(float(item["product_data/price"])) > 45 and int(float(item["product_data/price"])) <= 50 :
            range4550 += 1
    except:
        pass
    try:
        if int(float(item["product_data/price"])) > 50 and int(float(item["product_data/price"])) <= 100 :
            range50100 += 1
    except:
        pass
    try:
        if int(float(item["product_data/price"])) > 100 and int(float(item["product_data/price"])) <= 200 :
            range100200 += 1
    except:
        pass
    try:
        if int(float(item["product_data/price"])) > 200 and int(float(item["product_data/price"])) <= 300 :
            range200300 += 1
    except:
        pass
    try:
        if int(float(item["product_data/price"])) > 300 and int(float(item["product_data/price"])) <= 400 :
            range300400 += 1
    except:
        pass
    try:
        if int(float(item["product_data/price"])) > 400 and int(float(item["product_data/price"])) <= 500 :
            range400500 += 1
    except:
        pass

preiseArr = ["[0€ - 5€]","]5€ - 10€]","]10€ - 15€]","]15€ - 20€]","]20€ - 25€]","]25€ - 30€]","]30€ - 35€]","]35€ - 40€]","]40€ - 45€]","]45€ - 50€]","]50€ - 100 €]","]100€ - 200 €]","]200€ - 300€]","]300€ - 400€]","]400€ - 500€]"]

chart_data = pd.DataFrame({'Preisbereich': preiseArr, 
                           'Anzahl Produkte':[range05,range510,range1015,range1520,range2025,range2530,range3035,range3540,range4045,range4550,range50100,range100200,range200300,range300400,range400500]})

c = ( 
    alt.Chart(chart_data).mark_bar().encode(alt.X('Preisbereich',sort = preiseArr,axis=alt.Axis(labelAngle=0)) ,alt.Y('Anzahl Produkte',axis=alt.Axis(labelAngle=0)))
    )
st.altair_chart(c, use_container_width=True)
