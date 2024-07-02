import streamlit as st

create_page = st.Page("Startseite.py", title="Startseite")
attribute = st.Page("pages/Attribute_ausgefüllt.py", title="Completeness-Wert")
nutrition = st.Page("pages/Nährwert_Tabelle_2.3_FlattenAll.py", title="Nährwerttabelle")
gtin = st.Page("pages/Gtin.py" , title="Anzahl Produkte Gtin")
preis = st.Page("pages/Preis.py" , title="Preise")

pg = st.navigation({
    "Start" : [create_page],
    "Shops" : [attribute, gtin, preis],
    "Nährwerte" : [nutrition]
    

})


pg.run()