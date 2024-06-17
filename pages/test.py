import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.markdown('<style>.stSlider {background-color: coral;}</style>', unsafe_allow_html=True)
st.markdown('<footer> <p>Umweltcampus Birkenfeld</p> </p></footer>',unsafe_allow_html=True)
st.slider('hi',0,10)
