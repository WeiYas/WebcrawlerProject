import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="Hello",
    page_icon="👋",
)

col1, col2 = st.columns(2)

with col1:
    st.title("Willkommen zum Webcrawler Dashboard")
with col2:
    st.image('LogoUCB.jpg',width = 300)

st.markdown(
    """
    Wir sind nun auf der Startseite des Webcrawlers. 
    
    ### Ansicht wechseln?
    👈 Um die Ansicht zu wechseln, **wählen sie auf der Sidebar** eine Kategorie aus.
"""
)


