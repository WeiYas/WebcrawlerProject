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

# https://www.volgshop.ch/ , https://shop.rewe.de/ , "https://www.lidl.de/" , "https://www.supermarkt24h.de/" , "https://www.heinemann-shop.com/", "https://www.mega-einkaufsparadies.de/"

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["connection_string"]
    return pymongo.MongoClient(connection_string)

client = init_connection()

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

#SHOPS
@st.cache_data(ttl=600)
def get_data():
    db = client.mydb
    items = db.all_flatten.find({},{"_id":1, "shop_url" : 1})
    items = list(items)
    return items

@st.cache_data(ttl=600)
def get_data_no_flatten() :
    db = client.mydb
    items = db.mycollection.find({"completeness" : {"$exists" : True}},{"_id":0, "completeness":1, "shop_url" : 1})
    items = list(items)
    return items


items = get_data()
noFlatitems = get_data_no_flatten()

count, countE ,countV,countG ,countVo ,countR ,countL ,countS ,countH,countM = 0,0,0,0,0,0,0,0,0,0
countCompleteE, countCompleteV, countCompleteG ,countCompleteVo ,countCompleteR ,countCompleteL ,countCompleteS ,countCompleteH,countCompleteM = 0,0,0,0,0,0,0,0,0
choice = " keinem "

#Produkte zählen

#itemsEdeka, itemsVekoop, itemsGlobus, itemsVolg, itemsRewe, itemsLidl, itemsSuper, itemsHeine, itemsMega = []

#SHOPS ZÄHLEN
st.subheader("Übersicht Daten Shops")
for item in items:
    try : 
        if item["shop_url"] == "https://www.edeka24.de/" :
            countE += 1
    except:
        pass
    try : 
        if item["shop_url"] == "https://www.vekoop.de/" :
            countV += 1
    except:
        pass
    try : 
        if item["shop_url"] == "https://www.globus.de/" :
            countG += 1
    except:
        pass
    try : 
        if item["shop_url"] == "https://www.volgshop.ch/" :
            countVo += 1
    except:
        pass
    try : 
        if item["shop_url"] == "https://shop.rewe.de/" :
            countR += 1
    except:
        pass
    try : 
        if item["shop_url"] == "https://www.lidl.de/" :
            countL += 1
    except:
        pass
    try : 
        if item["shop_url"] == "https://www.supermarkt24h.de/" :
            countS += 1
    except:
        pass
    try : 
        if item["shop_url"] == "https://www.heinemann-shop.com/" :
            countH += 1
    except:
        pass
    try : 
        if item["shop_url"] == "https://www.mega-einkaufsparadies.de/" :
            countM += 1
    except:
        pass

#GTIN DURCHSCHNITT

for item in noFlatitems:
    try : 
        if item["shop_url"] == "https://www.edeka24.de/":
            countCompleteE += item["completeness"]
    except:
        pass
    try : 
        if item["shop_url"] == "https://www.vekoop.de/" :
            countCompleteV += item["completeness"]
            count = countV
    except:
        pass
    try : 
        if item["shop_url"] == "https://www.globus.de/" :
            countCompleteG += item["completeness"]
            count = countG
    except:
        pass
    try : 
        if item["shop_url"] == "https://www.volgshop.ch/" :
            countCompleteVo += item["completeness"]
            count = countVo
    except:
        pass
    try : 
        if item["shop_url"] == "https://shop.rewe.de/" :
            countCompleteR += item["completeness"]
            count = countR
    except:
        pass
    try : 
        if item["shop_url"] == "https://www.lidl.de/" :
            countCompleteL += item["completeness"]
            count = countL
    except:
        pass
    try : 
        if item["shop_url"] == "https://www.supermarkt24h.de/" :
            countCompleteS += item["completeness"]
            count = countS
    except:
        pass
    try : 
        if item["shop_url"] == "https://www.heinemann-shop.com/" :
            countCompleteH += item["completeness"]
            count = countH
    except:
        pass
    try : 
        if item["shop_url"] == "https://www.mega-einkaufsparadies.de/" :
            countCompleteM += item["completeness"]
            count = countM
    except:
        pass

if countE != 0 :
    countCompleteE = countCompleteE / countE
else : 
    countCompleteE = 0

if countV != 0 :
    countCompleteV = countCompleteV / countV
else : 
    countCompleteV = 0

if countVo != 0 :
    countCompleteVo = countCompleteVo / countVo
else : 
    countCompleteVo = 0

if countG != 0 :
    countCompleteG = countCompleteG / countG
else : 
    countCompleteG = 0

if countH != 0 :
    countCompleteH = countCompleteH / countH
else : 
    countCompleteH = 0

if countR != 0 :
    countCompleteR = countCompleteR / countR
else : 
    countCompleteR = 0

if countS != 0 :
    countCompleteS = countCompleteS / countS
else : 
    countCompleteS = 0

if countL != 0 :
    countCompleteL = countCompleteL / countL
else : 
    countCompleteL = 0

if countM != 0 :
    countCompleteM = countCompleteM / countM
else : 
    countCompleteM = 0


count = countE + countV + countG + countVo + countH + countL + countM + countS 

shopsName = ["Edeka", "Globus", "Vekoop", "Volg" , "Heinemann", "Mega-Einkaufsparadies","Rewe", "Supermarkt24h", "Lidl"]
produkteAnzahl = [countE, countG, countV, countVo, countH, countM,countR ,countS, countL]
averageComplete = [countCompleteE, countCompleteG ,countCompleteV, countCompleteVo ,countCompleteH,countCompleteM,countCompleteR  ,countCompleteS,countCompleteL ]

# --- TABELLE ---

dt = pd.DataFrame({
    "shopname" : shopsName ,
    "produkteAnzahl" :  produkteAnzahl,
    "averageComplete" : averageComplete
})
st.dataframe(dt,
            column_config={
                 "shopname":"Namen der Shops",
                 "produkteAnzahl" : "Anzahl Produkte",
                 "averageComplete" : "Durschnittliche Vollständigkeit"
            }, 
            hide_index = True,)
st.write("Anzahl aller Produkte insgesamt: ", str(count))

    