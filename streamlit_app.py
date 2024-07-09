import streamlit as st

create_page = st.Page("Startseite.py", title="Startseite")

attribute = st.Page("pages/completeness_allgemein.py", title="Completeness-Wert allgemein")
attributeShop = st.Page("pages/completeness_je_Shop.py", title="Completeness-Wert je Shop")

nutrition = st.Page("pages/Nährwert_Tabelle_2.3_FlattenAll.py", title="Nährwerttabelle")
nutrition_allgemein = st.Page("pages/Nährwerte_allgemein.py", title="Nährwerttabelle")

gtin_allgemein = st.Page("pages/Gtin_Allgemein.py" , title="GTIN je Produkte")
gtin_shop = st.Page("pages/Gtin_Shop.py" , title="GTIN je Shop")
preis = st.Page("pages/Preis.py" , title="Preise")

pg = st.navigation({
    "Start" : [create_page],
    "Übersicht" : [attribute, gtin_allgemein, preis, nutrition_allgemein],
    "Shops" : [attributeShop, gtin_shop, nutrition]
    

})

pg.run()