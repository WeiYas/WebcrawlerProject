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

@st.cache_data(ttl=600)
def get_data():
    db = client.mydb
    items = db.mycollection.find({}, {"_id" :0 , "product_data" : {"gtin" : 1}})
    items = list(items)
    return items

items = get_data()

countGtin = 0
countNogtin = 0

for item in items:
    countGtin += 1
    # st.write(item)
st.write(countGtin)

chart_data = pd.DataFrame({
  'name': ["ja","nein"],
  'number of products':[countGtin,countNogtin]
})

chart_data = chart_data.set_index('name')
st.bar_chart(chart_data)

