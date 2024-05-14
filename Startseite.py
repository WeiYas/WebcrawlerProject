import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    page_title="Startseite",
    page_icon="random",
)

col1, col2 = st.columns(2)

with col1:
    st.title("Willkommen zum Webcrawler Dashboard")
with col2:
    st.image('logo_ucb.png',width = 500)

st.markdown(
    """
    Wir sind nun auf der Startseite des Webcrawlers. 
    
    ### Ansicht wechseln?
    👈 Um die Ansicht zu wechseln, **wählen sie auf der Sidebar** eine Kategorie aus.
"""
)


