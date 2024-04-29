import streamlit as st
import pymongo
import pandas as pd

#App Title
st.title('your first mongoDB data visualization😎')

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()
db = client.universities_rank

@st.cache_data(ttl=600)
def get_universities():
    collection = db['universities'].find({})
    return pd.DataFrame(collection)

#disply the dataframe
universities = get_universities()
st.write(universities)