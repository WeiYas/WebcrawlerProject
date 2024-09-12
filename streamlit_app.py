import streamlit as st

create_page = st.Page("Startseite.py", title="Startseite")
search_page = st.Page("pages/Suche.py" , title="Suche")
attribute = st.Page("pages/completeness_allgemein.py", title="Completeness Allgemein")
attributeShop = st.Page("pages/completeness_je_Shop.py", title="Completeness Allgemein je Shop")

nutrition = st.Page("pages/Nährwert_Tabelle_2.3_FlattenAll.py", title="Completeness Nährwerttabelle je Shop")
nutrition_allgemein = st.Page("pages/Nährwerte_allgemein.py", title="Completeness Nährwerttabelle")

gtin_allgemein = st.Page("pages/Gtin_Allgemein.py" , title="Completeness GTIN")
gtin_shop = st.Page("pages/Gtin_Shop_copy.py" , title="Completeness GTIN je Shop")

preis = st.Page("pages/Preis.py" , title="Completeness Preise je Shop")
preis_allgemein = st.Page("pages/Preis_Bereich.py" , title="Completeness Preise")

pg = st.navigation({
    "Start" : [create_page, search_page],
    "Übersicht" : [attribute, gtin_allgemein, nutrition_allgemein,preis_allgemein],
    "Shops" : [attributeShop, gtin_shop, nutrition, preis]
    

})

pg.run()