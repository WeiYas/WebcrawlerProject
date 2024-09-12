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

with st.spinner('Daten werden geladen') :
    @st.cache_data(ttl=600,show_spinner = False)
    def get_data():
        db = client.mydb
        items = db.all_flatten.find({'$expr': { '$getField': 'product_data/gtin' }}, {"product_data/gtin" : 1})
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
        'GTIN vorhanden': ["ja","nein"],
        'Anzahl Produkte':[countGtin,countNoGtin]
        })
        # ANZEIGE AUF BROWSER

        
    st.write(" ")

    st.subheader("Wieviele Produkte besitzen einen GTIN?")

    container = st.container(border = True)
    with container:
            st.write("- Anzahl von Produkten mit GTIN: ", str(countGtin))
            st.write("- Anzahl von Produkten ohne GTIN: " , str(countNoGtin))

                #chart_data = chart_data.set_index('Gtin vorhanden')
                #st.bar_chart(chart_data)
    c = ( 
        alt.Chart(chart_data).mark_bar().encode(x='GTIN vorhanden',y='Anzahl Produkte')
        )
    st.altair_chart(c, use_container_width=True)


