import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(
    layout="wide",
    page_title="Startseite",
    page_icon="random"
)

st.markdown('<style>h1{font-size:25px;} h3{font-size:20px;}</style>', unsafe_allow_html=True)

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


st.markdown('<style> .footer{position: fixed;left: 0;bottom: 0;width: 100%;color: black;text-align: center;}</style> <div class="footer"><p>Umwelt-Campus Birkenfeld</p></div>',unsafe_allow_html=True)