import streamlit as st
import pymongo
import pandas as pd
import time
import matplotlib.pyplot as plt
import numpy as np
import altair as alt

st.title("Anzahl Produkte je Completeness-Bereich")
st.write(" ")
st.markdown('<style>h1{font-size:25px;} h3{font-size:20px;}</style>', unsafe_allow_html=True)

@st.cache_resource
def init_connection():
    return pymongo.MongoClient("mongodb://localhost:27017/")

client = init_connection()

# ----- Produkte Completeness -------

@st.cache_data(ttl=600)
def get_data():
    db = client.mydb
    items = db.mycollection.find({}, {"_id" :0, "completeness" : 1})
    items = list(items)
    return items

item = get_data()

count1 = 0
count2= 0
count3 = 0
count4 = 0
count5 = 0
count6 = 0
count7 = 0
count8 = 0
count9 = 0
count10 = 0

for items in item:
    if items["completeness"] <= 0.1 and items["completeness"] > 0.0 :
        count1 +=1     
    if items["completeness"] <= 0.2 and items["completeness"] > 0.1 :
        count2 +=1     
    if items["completeness"] <= 0.3 and items["completeness"] > 0.2 :
        count3 +=1
    if items["completeness"] <= 0.4 and items["completeness"] > 0.3 :
        count4 +=1     
    if items["completeness"] <= 0.5 and items["completeness"] > 0.4 :
        count5 +=1     
    if items["completeness"] <= 0.6 and items["completeness"] > 0.5 :
        count6 +=1     
    if items["completeness"] <= 0.7 and items["completeness"] > 0.6 :
        count7 +=1
    if items["completeness"] <= 0.8 and items["completeness"] > 0.7 :
        count8 +=1
    if items["completeness"] <= 0.9 and items["completeness"] > 0.8 :
        count9 +=1
    if items["completeness"] <= 1 and items["completeness"] > 0.9 :
        count10 +=1



chart_data = pd.DataFrame({'Completeness-Bereich': ["[0.0 - 0.1]","]0.1 - 0.2]", "]0.2 - 0.3]","]0.3 - 0.4]", "]0.4 - 0.5]", "]0.5 - 0.6]", "]0.6 - 0.7]", "]0.7 - 0.8]" , "]0.8 - 0.9]" , "]0.9 - 1.0]"], 'Anzahl Produkte':[count1,count2,count3,count4,count5,count6,count7,count8,count9,count10]})
    #chart_data = chart_data.set_index('completeness-value')
    # st.bar_chart(chart_data)
c = ( 
    alt.Chart(chart_data).mark_bar().encode(alt.X('Completeness-Bereich',axis=alt.Axis(labelAngle=0)) ,alt.Y('Anzahl Produkte',axis=alt.Axis(labelAngle=0)))
    )
st.altair_chart(c, use_container_width=True)

st.markdown('<style> .footer{position: fixed;left: 0;bottom: 0;width: 100%;color: black;text-align: center;}</style> <div class="footer"><p>Umwelt-Campus Birkenfeld</p></div>',unsafe_allow_html=True)


# -- MEDIAN -- 
median = 0
list_complete = []

for i in item :
    try:
        if i["completeness"] :
            list_complete.append(i["completeness"])
    except:
        pass

list_complete.sort()
#print(list_complete)

n = len(list_complete)

if n%2 == 0 :
    median = (list_complete[int(n/2)-1] + list_complete[int((n+1)/2+0.5)-1])/2

else:
    median = list_complete[int((n+1)/2)-1]
print(median)

# -- Quartile

q1 = 0
q2= median
q3 = 0

q1 = n * 0.25
q3 = n * 0.75

q1,q2,q3 = np.percentile(list_complete, [25,50,75])

q = [round(q1,2),round(q2,2),round(q3,2)]
quartile = ["Q1","Q2","Q3"]

st.subheader("Quartile und Median")

dt = pd.DataFrame({
    "quartile" : quartile ,
    "wert" :  q
})

st.dataframe(dt,
            column_config={
                "quartile":"Quartile",
                "wert" : " ",
            }, 
            hide_index = True,)
st.write("Q2 = Median")