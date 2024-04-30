import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np

values = st.slider(
    'Select a price',
    0.0, 100.0, (0.1, 100.0))
st.write('Values:', values)

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()

@st.cache_data(ttl=600)
def get_data():
    db = client.mydb
    items = db.mycollection.find({"product_data" : {"price":"4.29"}})
    items = list(items)
    return items

items = get_data()

for item in items:
    st.write(item)

