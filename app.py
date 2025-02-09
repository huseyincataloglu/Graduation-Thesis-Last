
import numpy as np
import pandas as pd
import streamlit as st
import plotly.express as px
from modules.datacleaning import clean_data
from modules import visualization as viz
from modules import utilities as util

st.set_page_config(
    page_title="FishStats Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)
    

# Veri yükleme
df = pd.read_csv('data/FishStats2018_cleaned.csv')


# Başlık
st.markdown("<h1 style = 'text-align: center; color : red;'>FishStats Dashboard </h1>",unsafe_allow_html=True)

st.markdown("""
    <h2 style="font-size:26px;">Welcome to the <strong style="color:red;">FishStats Dashboard</strong>!</h2>
    <p style="font-size:20px;">This <strong style="color:red;">Streamlit</strong> dashboard is built to visualize the global fish catch dataset from <a href="https://www.kaggle.com/datasets/thebumpkin/worldwide-fishing-catch-statitstics-1950-2018" target="_blank">Kaggle</a>.</p>        
    <p style="font-size:20px;">In this main page, you can explore the general information and the dataset. For more detailed analysis, you can access other pages via the sidebar!<p>
    """, 
    unsafe_allow_html=True
)

st.write("-----------------------")
st.markdown("""
    <h1 style="font-size:26px;">Exploring the Dataset</h2>
    """, unsafe_allow_html=True)
# Genel Bilgiler
rows,cols = df.shape
col1, col2, col3 ,col4= st.columns(4)
with col1:
    st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        border: 2px solid blue; 
        padding: 10px;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    st.metric(label="Number of Countries 🌍",value=f"{util.get_total_features(df,"Country")}")
    st.metric(label="Dataset Shape", value=f"{rows} rows", delta=f"{cols} columns")

with col2:
    st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        border: 2px solid blue; /* Yeşil çerçeve */
        padding: 10px;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    st.metric("Number of Species :fish:",f"{util.get_total_features(df,"Species")}")


with col3:
    st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        border: 2px solid blue; /* Yeşil çerçeve */
        padding: 10px;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    st.metric("All Locations 🗺️",f"{util.get_total_features(df,"Location")}")

with col4:
    st.markdown(
    """
    <style>
    div[data-testid="stMetric"] {
        border: 2px solid blue; /* Yeşil çerçeve */
        padding: 10px;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    </style>
    """,
    unsafe_allow_html=True
    )
    st.metric("All Production Methods",f"{util.get_total_features(df,"Detail")}")


st.dataframe(df)

cc1,_,cc2 = st.columns([1,0.2,1])
with cc1:
    a,b = st.columns([1,2])
    with a:
        st.subheader("Missing values ")
        st.dataframe((df.isnull().sum() / len(df) * 100).reset_index(name="Propotion"))
    with b:
        st.subheader("Describing Numerical Columns")
        st.dataframe(df.describe())

    allzeros = df[(df[df.columns[4:]] == 0).all(axis = 1)]
   
with cc2:
    st.subheader("Some arrangements in dataset :")
    production_mapping = {
        "Capture production": "Capture",
        "Aquaculture production (marine)": "Marine Aq",
        "Aquaculture production (freshwater)": "Freshwater Aq",
        "Aquaculture production (brackishwater)": "Brackish Aq"
        }
    st.write("In detail column, The name of production methods can be minimized for efficency and readablity")
    st.write(production_mapping)




st.write("--------------------")

st.markdown("## <span style='color:red;'>🌍 FAO Fisheries Area Map</span>", unsafe_allow_html=True)

st.write("""
The FAO (Food and Agriculture Organization) defined fisheries areas are used to classify water bodies across the world.  
Select a region from the menu below to view the corresponding map.
""")
c1,c2 = st.columns([2,1])
with c1:
    choose = st.selectbox("Choose fishery area :",options=list(df.Location.unique()))
    if choose == "Africa - Inland waters":
        st.image("assets/africa_inland waters.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Asia - Inland waters":
        st.image("assets/Asia_inland_waters.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Mediterranean and Black Sea":
        st.image("assets/Mediterrian_and_black_sea.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Europe - Inland waters":
        st.image("assets/euroe_inlandwaters.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Pacific, Eastern Central":
        st.image("assets/pacific_eastern.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Oceania - Inland waters":
        st.image("assets/ocenia_inland_waters.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Atlantic, Southeast":
        st.image("assets/atlantic_southeast.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Atlantic, Eastern Central":
        st.image("assets/atlantic_eastern.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Atlantic, Western Central":
        st.image("assets/atlantic_western.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "America, North - Inland waters":
        st.image("assets/america_north_inland.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "America, South - Inland waters":
        st.image("assets/america_southinland.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Atlantic, Antarctic":
        st.image("assets/atlantic_antartic.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Atlantic, Southwest":
        st.image("assets/Atlantic_ Southwest.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Pacific, Antarctic":
        st.image("assets/pacific_antartic.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Indian Ocean, Antarctic":
        st.image("assets/Indian Ocean_Antarctic.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Indian Ocean, Eastern":
        st.image("assets/Indian Ocean_Eastern.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Pacific, Southwest":
        st.image("assets/Pacific_Southwest.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Pacific, Western Central":
        st.image("assets/Pacific_Western Central.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Indian Ocean, Western":
        st.image("assets/Indian Ocean_Western.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Atlantic, Northeast":
        st.image("assets/Atlantic_Northeast.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Pacific, Southeast":
        st.image("assets/Pacific_Southeast.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Atlantic, Northwest":
        st.image("assets/Atlantlic_northwest.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Pacific, Northeast":
        st.image("assets/Pacific_Northeast.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Pacific, Northwest":
        st.image("assets/Pacific_Northwest.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)
    elif choose == "Arctic Sea":
        st.image("assets/Arctic Sea.gif", caption="FAO Balıkçılık Bölgeleri Haritası", width=800)


df = clean_data(df)