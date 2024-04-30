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

st.title("Willkommen zum Webcrawler Dashboard")

st.markdown(
    """
    Wir sind nun auf der Startseite des Webcrawlers. 
    
    ### Ansicht wechseln?
    👈 Um die Ansicht zu wechseln, **wählen sie auf der Sidebar** eine Kategorie aus.
"""
)


